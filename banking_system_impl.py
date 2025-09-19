import collections
from trepan.api import debug

class BankingSystemImpl:
    """
    A simplified banking system that supports account creation, deposits, transfers,
    and scheduled payments.
    """

    def __init__(self):
        """
        Initializes the banking system.
        - accounts: Stores account data, mapping account_id to {'balance': int, 'spent': int}.
        - scheduled_payments: Stores scheduled payment data, mapping payment_id to its details.
        - payment_counter: A counter to generate unique payment IDs.
        """
        self.accounts = {}
        self.scheduled_payments = {}
        self.payment_counter = 0

    def _process_pending_events(self, timestamp: int):
        """
        Processes all scheduled payments that should have occurred by the given timestamp.
        This is the core logic for the time-based event system.
        """
        # Identify all payments that are pending and due for execution.
        pending_due_payments = []
        for payment_id, details in self.scheduled_payments.items():
            if details['status'] == 'PENDING' and details['exec_time'] <= timestamp:
                pending_due_payments.append((payment_id, details))

        # Sort payments first by execution time, then by creation order (using the payment_id number).
        pending_due_payments.sort(key=lambda p: (p[1]['exec_time'], int(p[0][7:])))

        # Process each sorted payment.
        for payment_id, details in pending_due_payments:
            account_id = details['account_id']
            amount = details['amount']
            account = self.accounts.get(account_id)

            # A payment is skipped if the account has insufficient funds.
            if account and account['balance'] >= amount:
                account['balance'] -= amount
                account['spent'] += amount  # Successful payments count towards top_spenders.
                self.scheduled_payments[payment_id]['status'] = 'COMPLETED'
            else:
                # Also handles cases where the account might have been deleted (not in spec but good practice).
                self.scheduled_payments[payment_id]['status'] = 'SKIPPED'

    # --------------------------------------------------------------------------
    # Level 1 Methods
    # --------------------------------------------------------------------------

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._process_pending_events(timestamp)
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = {'balance': 0, 'spent': 0}
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._process_pending_events(timestamp)
        if account_id not in self.accounts or amount < 0:
            return None
        self.accounts[account_id]['balance'] += amount
        return self.accounts[account_id]['balance']

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        self._process_pending_events(timestamp)
        
        # Validate transfer conditions
        if (source_account_id not in self.accounts or
                target_account_id not in self.accounts or
                source_account_id == target_account_id or
                amount <= 0 or
                self.accounts[source_account_id]['balance'] < amount):
            return None

        # Perform the transfer
        self.accounts[source_account_id]['balance'] -= amount
        self.accounts[target_account_id]['balance'] += amount
        
        # Update the total amount spent for the source account (for Level 2)
        self.accounts[source_account_id]['spent'] += amount
        
        return self.accounts[source_account_id]['balance']

    # --------------------------------------------------------------------------
    # Level 2 Method
    # --------------------------------------------------------------------------

    def top_spenders(self, timestamp: int, num_accounts: int) -> list[str]:
        self._process_pending_events(timestamp)
        
        # Filter out accounts that have not spent anything.
        spenders = [
            (acc_id, data) for acc_id, data in self.accounts.items() if data['spent'] > 0
        ]
        
        # Sort by amount spent (descending), with account_id (lexicographically ascending) as a tie-breaker.
        spenders.sort(key=lambda item: (-item[1]['spent'], item[0]))
        
        # Return the top N account IDs.
        return [acc_id for acc_id, data in spenders[:num_accounts]]

    # --------------------------------------------------------------------------
    # Level 3 Methods
    # --------------------------------------------------------------------------

    def schedule_payment(self, timestamp: int, account_id: str, amount: int, delay: int) -> str | None:
        self._process_pending_events(timestamp)
        
        if account_id not in self.accounts or amount <= 0 or delay < 0:
            return None
            
        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"
        
        self.scheduled_payments[payment_id] = {
            'account_id': account_id,
            'amount': amount,
            'exec_time': timestamp + delay,
            'status': 'PENDING'
        }
        return payment_id

    def cancel_payment(self, timestamp: int, account_id: str, payment_id: str) -> bool:
        # Per specification, payments at the given timestamp are processed before cancellations.
        self._process_pending_events(timestamp)

        payment = self.scheduled_payments.get(payment_id)

        # Cancellation fails if payment doesn't exist, belongs to another account, or is not pending.
        if (not payment or
                payment['account_id'] != account_id or
                payment['status'] != 'PENDING'):
            return False

        payment['status'] = 'CANCELED'
        return True
