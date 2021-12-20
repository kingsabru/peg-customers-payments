use peg;

-- customer table
alter table customer
add primary key (CustomerId);

-- product table
alter table product
add primary key (ProductId);

SET SQL_SAFE_UPDATES = 0;
update contract set ProductId = 3 where ProductId = 0;
SET SQL_SAFE_UPDATES = 1;

insert into product(ProductId, Name, Price, `Product type`) values (3, 'Unknown', 0, 'Unknown');

-- contract table
alter table contract
add primary key (ContractId);

ALTER table contract
ADD CONSTRAINT fk_CustomerId
FOREIGN KEY (CustomerId)
REFERENCES customer(CustomerId)
ON DELETE cascade
ON UPDATE cascade;

ALTER table contract
ADD CONSTRAINT fk_ProductId
FOREIGN KEY (ProductId)
REFERENCES product(ProductId)
ON DELETE cascade
ON UPDATE cascade;

-- transactions table
ALTER table transactions
ADD CONSTRAINT fk_ContractId
FOREIGN KEY (contractid)
REFERENCES contract(ContractId)
ON DELETE cascade
ON UPDATE cascade;

ALTER table transactions
ADD CONSTRAINT fk_CustomerId_Transactions
FOREIGN KEY (customerid)
REFERENCES customer(CustomerId)
ON DELETE cascade
ON UPDATE cascade;