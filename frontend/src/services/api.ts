import type { InfrastructureItem } from "@/types/infrastructure";
import { useFetch } from "@vueuse/core";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Standardize URL formatting
const getUrl = (path: string) => `${API_URL}${path}`.replace(/([^:]\/)\/+/g, "$1");

/**
 * Composable to fetch the entire infrastructure tree.
 * Returns reactive { data, isFetching, error, execute }
 */
export const useInfrastructure = () => {
  const url = getUrl("/infrastructure/");
  return useFetch(url, {
    immediate: true, 
  }).get().json<InfrastructureItem[]>();
};

/**
 * Composable to fetch a single infrastructure item by ID.
 * Returns reactive { data, isFetching, error, execute }
 */
export const useInfrastructureItem = (id: number) => {
  const url = getUrl(`/infrastructure/${id}`);
  return useFetch(url, {
    immediate: true,
  }).get().json<InfrastructureItem>();
};

// --- Actions (Create, Update, Delete) are kept as async functions for imperative usage ---

export const createInfrastructureItem = async (item: Partial<InfrastructureItem>): Promise<InfrastructureItem> => {
    const url = getUrl("/infrastructure/");
    const { data, error } = await useFetch(url)
        .post(item)
        .json<InfrastructureItem>();

    if (error.value) {
        // Parse error similar to before
        let errorMessage = `Failed to create item`;
        const errorData = data.value as any;
        if (errorData?.detail) {
             if (Array.isArray(errorData.detail)) {
                 errorMessage = errorData.detail.map((e: any) => e.msg).join(", ");
             } else {
                 errorMessage = errorData.detail;
             }
         }
         throw new Error(errorMessage);
    }
    return data.value!;
};

export const deleteInfrastructureItem = async (id: number): Promise<void> => {
    const url = getUrl(`/infrastructure/${id}`);
    const { error } = await useFetch(url).delete();

    if (error.value) {
        throw new Error(`Failed to delete item: ${error.value}`);
    }
};

export const updateInfrastructureItem = async (id: number, item: Partial<InfrastructureItem>): Promise<InfrastructureItem> => {
    const url = getUrl(`/infrastructure/${id}`);
    const { data, error } = await useFetch(url)
        .put(item)
        .json<InfrastructureItem>();

    if (error.value) {
        let errorMessage = `Failed to update item`;
        const errorData = data.value as any;
        if (errorData?.detail) {
            if (Array.isArray(errorData.detail)) {
                errorMessage = errorData.detail.map((e: any) => e.msg).join(", ");
            } else {
                errorMessage = errorData.detail;
            }
        }
        throw new Error(errorMessage);
    }
    return data.value!;
};
