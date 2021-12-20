use peg;

-- 2.	The target table should be filterable by:
-- a.	Type of product.
-- b.	Country.
-- c.	Contract status.
-- d.	Date
-- 3.	Don’t consider contracts with a status of RETURNED

CREATE TABLE customerpayments
SELECT t.customerid, t.contractid , p.Name, p.`Product type`, t.countryid, t.contractstatus, t.sum_paid_to_date, t.expectedtotalamount, t.Date
FROM peg.transactions t
	JOIN peg.contract co ON t.contractid = co.ContractId
    JOIN peg.customer cu ON t.customerid = cu.CustomerId
    JOIN peg.product p ON co.ProductId = p.ProductId
WHERE t.contractstatus <> "RETURNED";

-- Alternatives: SELECT INTO or INSERT INTO 

-- NOTES:
-- * Contract table had a foreign key of 0 for some productId(s). 
-- * Changed all 0s to 3s in ProductId column in contract table, inserted fake product details for ProductId 3 and created foreign key constraint