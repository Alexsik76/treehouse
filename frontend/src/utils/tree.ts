import type { InfrastructureItem } from "@/types/infrastructure";

/**
 * Recursively searches for an item with the specific ID in the infrastructure tree.
 */
export const findItemById = (
  items: InfrastructureItem[],
  id: number
): InfrastructureItem | null => {
  for (const item of items) {
    if (item.id === id) {
      return item;
    }
    if (item.children && item.children.length > 0) {
      const found = findItemById(item.children, id);
      if (found) {
        return found;
      }
    }
  }
  return null;
};
