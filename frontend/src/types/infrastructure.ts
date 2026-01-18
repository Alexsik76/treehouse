export const InfrastructureType = {
    SERVER: "server",
    VM: "vm",
    CONTAINER: "container",
    SWITCH: "switch",
    ROUTER: "router",
    OTHER: "other"
} as const;

export type InfrastructureType = typeof InfrastructureType[keyof typeof InfrastructureType];

export interface InfrastructureItem {
    id: number;
    name: string;
    type: InfrastructureType;
    ip_address?: string | null;
    dns_name?: string | null;
    specs: Record<string, any>;
    children: InfrastructureItem[];
    parent_id?: number | null;
}

export type InfrastructureItemCreate = Omit<InfrastructureItem, 'id' | 'children'>;
