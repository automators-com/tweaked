export function lookupTableName(id: string, tables: any[]): string {
  return tables.find((table) => table.id === id)?.table_name;
}
