export interface Transaction {
  id: number;
  accountId: number;
  type: "Credit" | "Debit";
  date: string;
  amount: number;
  description: string;
}
