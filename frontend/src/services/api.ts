import type { InfrastructureItem } from "@/types/infrastructure";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const fetchInfrastructure = async (): Promise<InfrastructureItem[]> => {
    try {
        const url = `${API_URL}/infrastructure/`.replace(/([^:]\/)\/+/g, "$1"); // Remove double slashes
        const response = await fetch(url, { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        const data = await response.json();
        return data as InfrastructureItem[];
    } catch (error) {
        console.error("Failed to fetch infrastructure:", error);
        throw error;
    }
};

export const createInfrastructureItem = async (item: Partial<InfrastructureItem>): Promise<InfrastructureItem> => {
    try {
        const url = `${API_URL}/infrastructure/`.replace(/([^:]\/)\/+/g, "$1");
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(item),
        });
        if (!response.ok) {
            let errorMessage = `Failed to create item: ${response.statusText}`;
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                   // If detail is a list (Pydantic validation error), format it
                   if (Array.isArray(errorData.detail)) {
                       errorMessage = errorData.detail.map((e: any) => e.msg).join(", ");
                   } else {
                       errorMessage = errorData.detail;
                   }
                }
            } catch (jsonError) {
                // Ignore JSON parse error, use fallback
            }
            throw new Error(errorMessage);
        }
        return await response.json();
    } catch (error) {
        console.error("Error creating item:", error);
        throw error;
    }
};

export const deleteInfrastructureItem = async (id: number): Promise<void> => {
    try {
        const url = `${API_URL}/infrastructure/${id}`.replace(/([^:]\/)\/+/g, "$1");
        const response = await fetch(url, {
            method: "DELETE",
        });
        if (!response.ok) {
            throw new Error(`Failed to delete item: ${response.statusText}`);
        }
    } catch (error) {
        console.error("Error deleting item:", error);
        throw error;
    }
};

export const updateInfrastructureItem = async (id: number, item: Partial<InfrastructureItem>): Promise<InfrastructureItem> => {
    try {
        const url = `${API_URL}/infrastructure/${id}`.replace(/([^:]\/)\/+/g, "$1");
        const response = await fetch(url, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(item),
        });
        if (!response.ok) {
            let errorMessage = `Failed to update item: ${response.statusText}`;
            try {
                const errorData = await response.json();
                 if (errorData.detail) {
                   if (Array.isArray(errorData.detail)) {
                       errorMessage = errorData.detail.map((e: any) => e.msg).join(", ");
                   } else {
                       errorMessage = errorData.detail;
                   }
                }
            } catch (jsonError) {
                // Ignore JSON parse error
            }
            throw new Error(errorMessage);
        }
        return await response.json();
    } catch (error) {
        console.error("Error updating item:", error);
        throw error;
    }
};

export const fetchInfrastructureItemById = async (id: number): Promise<InfrastructureItem> => {
    try {
        const url = `${API_URL}/infrastructure/${id}`.replace(/([^:]\/)\/+/g, "$1");
        const response = await fetch(url, { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Failed to fetch item ${id}:`, error);
        throw error;
    }
};
