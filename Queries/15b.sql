-- using 1733343690 as a seed to the RNG
EXPLAIN ANALYZE
with revenue_STREAM_ID (supplier_no, total_revenue) as (
	select
		l_suppkey,
		sum(l_extendedprice * (1 - l_discount))
	from
		lineitem
	where
		l_shipdate >= date '1996-06-01'
		and l_shipdate < date '1996-06-01' + interval '3' month
	group by
		l_suppkey)


select
	s_suppkey,
	s_name,
	s_address,
	s_phone,
	total_revenue
from
	supplier,
	revenue_STREAM_ID
where
	s_suppkey = supplier_no
	and total_revenue = (
		select
			max(total_revenue)
		from
			revenue_STREAM_ID
	)
order by
	s_suppkey;
