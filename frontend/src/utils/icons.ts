export const getOsIcon = (osName: string | undefined): string => {
  if (!osName) return "mdi-server";
  
  const os = osName.toLowerCase();
  
  const validMap: Record<string, string> = {
    "debian": "mdi-debian",
    "ubuntu": "mdi-ubuntu",
    "windows": "mdi-microsoft-windows",
    "fedora": "mdi-fedora",
    "rocky": "mdi-linux",
    "home assistant": "mdi-home-assistant",
    "hass": "mdi-home-assistant",
    "proxmox": "mdi-server-network",
  };

  // Check for exact matches or matches where the key is contained in the string
  for (const [key, icon] of Object.entries(validMap)) {
    if (os.includes(key)) {
      return icon;
    }
  }

  return "mdi-server";
};
