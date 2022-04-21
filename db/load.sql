\COPY Users FROM 'generated/Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq', 201, false);
\COPY Sellers FROM 'generated/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'generated/Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_product_id_seq', 501, false);
\COPY Purchases FROM 'generated/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_order_id_seq', 101, false);
\COPY ProductReviews FROM 'generated/ProductReviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerReviews FROM 'generated/SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY CartEntries FROM 'generated/CartEntries.csv' WITH DELIMITER ',' NULL '' CSV
\COPY OrderedItems FROM 'generated/OrderedItems.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SavedForLater FROM 'generated/SavedForLater.csv' WITH DELIMITER ',' NULL '' CSV