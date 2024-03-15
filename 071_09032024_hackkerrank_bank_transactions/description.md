Hackkerrank: 

In a day, an account holder at HackerBank wants to make n transactions. In each transaction, money is either sent (negative amount) or received (positive amount). Given n transactions, the transactions occur in order from transaction 1 through transaction n, but transactions may be skipped. The balance starts at 0 and is the running sum of the selected transactions. It can never go negative.


Find out the maximum number of transactions possible.
Example
transaction = [3, 2, -5, -6, -1, 4]
One solution is to perform transactions 1, 2, 3, and 6. Transactions are 0 + 3 + 2 + (-5) + 4 and balances are [3, 5, 0, 4]. Return 4, the maximum number of transactions possible.


Function Description 
Complete the function maximizeTransactions in the editor below.
maximizeTransactions has the following parameter(s):
    int transaction[n]:  the transaction amounts
Returns
    int: the maximum number of transactions possible
    
Constraints
1 ≤ n ≤ 2000
-109 ≤ transaction[i] ≤ 109, 0 ≤ i < n