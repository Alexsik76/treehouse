import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import select
from src.database import Base, SessionLocal, engine
from src.models.infrastructure import InfrastructureItem, InfrastructureType
from src.security import decrypt_data, encrypt_data

# Load env vars
load_dotenv()

async def verify_backend():
    print("--- Starting Backend Verification ---")
    
    # 1. Verify Encryption
    print("\n[1] Testing Security Module...")
    secret = "SuperSecretPassword123"
    token = encrypt_data(secret)
    decrypted = decrypt_data(token)
    
    print(f"Original: {secret}")
    print(f"Encrypted: {token}")
    print(f"Decrypted: {decrypted}")
    
    if secret == decrypted:
        print("✅ Encryption/Decryption Works!")
    else:
        print("❌ Encryption Failed!")
        return

    # 2. Verify Database
    print("\n[2] Testing Database...")
    
    # Reset tables (careful in prod, ok for dev verify)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created.")

    async with SessionLocal() as session:
        # Create Root Server
        specs = {
            "os": "Ubuntu 22.04",
            "ram": "32GB", 
            "root_password": encrypt_data("secure_root_pass")
        }
        
        server = InfrastructureItem(
            name="Primary-Server",
            type=InfrastructureType.SERVER,
            ip_address="192.168.1.10",
            specs=specs
        )
        
        session.add(server)
        await session.commit()
        await session.refresh(server)
        print(f"✅ Created Item: {server.name}") 

        # Create Child VM
        vm_specs = {"os": "Debian 12", "vcpus": 4}
        vm = InfrastructureItem(
            name="Docker-VM",
            type=InfrastructureType.VM,
            parent_id=server.id,
            specs=vm_specs
        )
        session.add(vm)
        await session.commit()
        await session.refresh(vm)
        print(f"✅ Created Child Item: {vm.name}")

        # Query with Eager Loading (The FIX)
        # Query Parent
        stmt = select(InfrastructureItem).where(InfrastructureItem.name == "Primary-Server")
        result = await session.execute(stmt)
        fetched_server = result.scalar_one()
        
        print(f"Fetched Parent: {fetched_server.name}")
        
        # Verify children via direct query (Safe & Reliable)
        # This avoids 'MissingGreenlet' errors common in ad-hoc async scripts on Windows
        stmt_children = select(InfrastructureItem).where(InfrastructureItem.parent_id == fetched_server.id)
        result_children = await session.execute(stmt_children)
        children = result_children.scalars().all()
        
        child_names = [child.name for child in children]
        print(f"Fetched Children: {child_names}")
        
        # Verify JSON encrypt
        decrypted_pass = decrypt_data(fetched_server.specs["root_password"])
        print(f"Decrypted Spec Password: {decrypted_pass}")
        
        if decrypted_pass == "secure_root_pass":
             print("✅ Spec Encryption Verified!")
        else:
             print("❌ Spec Encryption Failed!")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_backend())