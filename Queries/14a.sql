-- using 1733319430 as a seed to the RNG

EXPLAIN ANALYZE
select
	100.00 * sum(case
		when p_type like 'PROMO%'
			then l_extendedprice * (1 - l_discount)
		else 0
	end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from
	lineitem,
	part
where
	l_partkey = p_partkey
	and l_shipdate >= date '1996-11-01'
	and l_shipdate < date '1996-11-01' + interval '1' month;
