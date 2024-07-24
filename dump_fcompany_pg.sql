--
-- PostgreSQL database dump
--

-- Dumped from database version 14.12 (Ubuntu 14.12-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.12 (Ubuntu 14.12-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: act; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.act (
    id integer NOT NULL,
    id_act integer NOT NULL,
    date_act text NOT NULL,
    name_work text NOT NULL,
    price_work integer NOT NULL
);


ALTER TABLE public.act OWNER TO postgres;

--
-- Name: act_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.act_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.act_id_seq OWNER TO postgres;

--
-- Name: act_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.act_id_seq OWNED BY public.act.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    name text NOT NULL,
    profession text NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employees_id_seq OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.log (
    id integer NOT NULL,
    date_order text NOT NULL,
    name_customer text NOT NULL,
    brand_car text NOT NULL,
    year_car text NOT NULL,
    number_car text NOT NULL,
    text_order text NOT NULL,
    id_act integer
);


ALTER TABLE public.log OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.log_id_seq OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.log_id_seq OWNED BY public.log.id;


--
-- Name: stock_minus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock_minus (
    id integer NOT NULL,
    name text NOT NULL,
    quantity integer NOT NULL,
    price_unit integer NOT NULL,
    id_act integer NOT NULL
);


ALTER TABLE public.stock_minus OWNER TO postgres;

--
-- Name: stock_minus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stock_minus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stock_minus_id_seq OWNER TO postgres;

--
-- Name: stock_minus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stock_minus_id_seq OWNED BY public.stock_minus.id;


--
-- Name: stock_plus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock_plus (
    id integer NOT NULL,
    name text NOT NULL,
    quantity integer NOT NULL,
    price_unit integer NOT NULL
);


ALTER TABLE public.stock_plus OWNER TO postgres;

--
-- Name: stock_plus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stock_plus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stock_plus_id_seq OWNER TO postgres;

--
-- Name: stock_plus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stock_plus_id_seq OWNED BY public.stock_plus.id;


--
-- Name: act id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.act ALTER COLUMN id SET DEFAULT nextval('public.act_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log ALTER COLUMN id SET DEFAULT nextval('public.log_id_seq'::regclass);


--
-- Name: stock_minus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_minus ALTER COLUMN id SET DEFAULT nextval('public.stock_minus_id_seq'::regclass);


--
-- Name: stock_plus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_plus ALTER COLUMN id SET DEFAULT nextval('public.stock_plus_id_seq'::regclass);


--
-- Data for Name: act; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.act (id, id_act, date_act, name_work, price_work) FROM stdin;
162	1	17-01-2024	диагностика	150
163	2	17-01-2024	замена масла	100
164	1	17-01-2024	замена подшипника	100
165	1	17-01-2024	замена ступицы	250
166	2	17-01-2024	замена масла	100
167	6	19-01-2024	компьютерная диагностика	150
168	6	19-01-2024	замена масла	150
169	6	19-01-2024	замена фильтра масляного	100
170	3	18-01-2024	диагностика тормозной системы	150
171	3	18-01-2024	замена колодок тормозных	150
172	3	18-01-2024	замена дисков тормозных	250
173	3	18-01-2024	прокачка тормозной системы	100
174	5	19-01-2024	диагностика	150
175	5	19-01-2024	замена тяги рулевой	200
176	5	19-01-2024	замена тнаконечника рулевого управления	250
177	4	18-01-2024	замена пыльника рейки рулевой	200
178	7	20-01-2024	компьютерная диагностика	150
179	7	20-01-2024	ручная диагностика	100
180	7	20-01-2024	замена стартера	150
181	8	20-01-2024	замена масла	150
182	8	20-01-2024	замена фильтров (масляного, воздушного, салона)	300
183	9	20-01-2024	компьютерная диагностика	150
184	9	20-01-2024	замена свечей зажигания	200
185	9	20-01-2024	высверливание свечи	300
186	10	21-01-2024	диагностика	100
187	10	21-01-2024	ремонт глушителя	200
190	15	21-01-2024	замена антифриза	200
191	14	22-01-2024	замена масла	100
192	14	22-01-2024	замена фильтров (масляного, топливного, салона, воздушного)	300
193	14	22-01-2024	замена антифриза	100
194	13	22-01-2024	замена ремня ГРМ	400
195	17	23-01-2024	замена масла	100
196	17	23-01-2024	замена фильтра	150
197	16	22-01-2024	замена дисков, колодок	300
198	16	22-01-2024	замена масла	100
199	16	22-01-2024	замена фильтра	150
200	12	22-01-2024	замена антифриза	150
201	18	23-01-2024	компьютерная диагностика	150
202	18	23-01-2024	ручная диагностика	100
203	19	23-01-2024	компьютерная диагностика	150
204	19	23-01-2024	замена фильтра салона	50
205	11	21-01-2024	ручная диагностика электрики	200
107	19	23-01-2024	компьютерная диагностика	150
108	19	23-01-2024	замена фильтра салона	50
206	11	21-01-2024	замена аккумулятора	100
207	11	21-01-2024	замена свечей зажигания	200
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, name, profession) FROM stdin;
1	Васечкин А.В.	директор
3	Маркова А.И.	главный бухгалтер
4	Иванов И.И.	мастер участка № 1
5	Петров П.П.	мастер участка № 2
7	Бортников В.Л.	слесарь 5 разряда
8	Кузьмин А.П.	слесарь 5 разряда
9	Левкович А.Г.	слесарь 4 разряда
10	Орлов А.Л.	слесарь-электрик
6	Венско А.П.	слесарь-электрик
\.


--
-- Data for Name: log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.log (id, date_order, name_customer, brand_car, year_car, number_car, text_order, id_act) FROM stdin;
2	17-01-2024	Савельев Н.С.	Hyundai Matrix	2019	47-64 АВ4	Замена масла	2
3	17-01-2024	Трифонов А.А.	Citroen C5	2018	54-98 IB4	Стук в правом колесе, компьютерная диагностика, замена масла и фильтра масляного.	6
4	18-01-2024	Степанов В.В.	Audi A8 	2018	69-87 АВ4	Характерный звук при торможении и снижении скорости	3
5	18-01-2024	Якимович А.И.	Chevrolet Captiva	2017	78-56 IB4	Замена пыльника	4
7	20-01-2024	Антонов М.С.	Kia Sorento	2014	62-94 IB4	Не заводится	7
8	20-01-2024	Миронов К.П.	Opel Astra	2015	75-24 АВ4	Замена масла, фильтров : воздушного, масляного, салона	8
9	20-01-2024	Васильев А.С.	Opel Vectra	2021	78-21 IB4	заводится через раз	9
10	21-01-2024	Осипов О.Н.	Subaru Forester	2010	36-54 OB4	Громко едет, диагностика глушителя (ремонт)	10
11	21-01-2024	Лазарев К.И.	Citroen C5	2020	21-58 IB4	Быстрая разрядка аккумулятора, слабый свет фар	11
12	21-01-2024	Матвеев А.С.	FORD Focus	2019	84-25 АВ4	Замена антифриза	15
13	22-01-2024	Михеев А.В.	Honda CR-V	2021	45-28 IB4	Регламентное ТО	14
14	22-01-2024	Данилов Д.И.	LADA Granta	2019	87-24 АВ4	Замена ремня ГРМ	13
15	22-01-2024	Колесников А.В.	Mercedes A W176	2020	49-21 АН4	Замена тормозной жидкости	12
16	22-01-2024	Евстигнеев А.А.	Mitsubishi	2018	44-28 IB4	Замена дисков тормозных	16
17	23-01-2024	Петров С.Т.	LADA PRIORA	2020	85-24 АВ4	Замена масла	17
18	23-01-2024	Аксенов В.С.	Peugeot 3008	2019	57-77 IB4	Не заводится	18
6	19-01-2024	Иванов И.И.	Honda CR-V	2015	54-48 IB4	Люфт руля	5
19	23-01-2024	Попов Р.Т.	Skoda Superb	2021	47-54 IB4	Компьютерная диагностика	19
1	17-01-2024	Сидоров А.А.	Ford S-MAX	2020	87-95 OB4	Гул в районе правого колеса, при повороте клонит в другую сторону	1
20	24-01-2024	Парфёнов И.В.	Citroen C5	2019	85-78 IB4	Компьютерная диагностика	\N
\.


--
-- Data for Name: stock_minus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stock_minus (id, name, quantity, price_unit, id_act) FROM stdin;
2	масло моторное	7	300	2
44	подшипник ступичный	1	140	1
45	ступица	1	220	1
46	гайка	4	20	1
47	сальник	4	10	1
48	масло моторное	6	300	6
49	фильтр масляный	1	150	6
52	колодки тормозные(к-кт)	1	200	3
53	диски тормозные (к-кт)	1	350	3
54	жидкость тормозная	1	50	3
57	наконечник рулевого управления	1	100	5
58	тяга рулевого управления	1	200	5
59	пыльник рейки рулевой	1	100	4
60	стартер	1	200	7
61	масло моторное	6	300	8
62	фильтр масляный	1	150	8
63	фильтр воздушный	1	150	8
64	фильтр салона	1	100	8
65	свечи зажигания	4	50	9
69		0	0	10
71	антифриз	5	250	15
72	масло моторное	7	300	14
73	фильтр масляный	1	150	14
74	фильтр топливный	1	150	14
75	фильтр воздушный	1	150	14
76	фильтр салона	0	100	14
77	антифриз	0	250	14
78	ремень ГРМ	1	300	13
84	масло моторное	6	300	17
85	фильтр масляный	-2	150	17
91	диски тормозные (к-кт)	2	350	16
92	гайка	4	20	16
93	колодки тормозные(к-кт)	2	200	16
94	масло моторное	6	300	16
95	фильтр масляный	1	150	16
96	антифриз	4	250	12
100		0	0	18
101	фильтр салона	1	100	19
148	аккумулятор	1	250	11
149	свечи зажигания	4	50	11
\.


--
-- Data for Name: stock_plus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stock_plus (id, name, quantity, price_unit) FROM stdin;
1	масло моторное	50	300
2	антифриз	20	250
8	фильтр масляный	10	150
10	фильтр топливный	8	150
11	фильтр салона	10	100
12	жидкость тормозная	10	50
13	ремень ГРМ	5	300
14	фильтр воздушный	10	150
15	стартер	2	200
16	колодки тормозные(к-кт)	8	200
17	подшипник ступичный	4	140
18	ступица	4	220
19	гайка	20	20
20	сальник	20	10
21	диски тормозные (к-кт)	6	350
22	пыльник рейки рулевой	4	100
23	тяга рулевого управления	2	200
24	наконечник рулевого управления	2	100
25	свечи зажигания	16	50
26	аккумулятор	2	250
27	масло моторное 10W-50	10	250
28	трансмиссионное масло	10	250
\.


--
-- Name: act_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.act_id_seq', 207, true);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 12, true);


--
-- Name: log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.log_id_seq', 35, true);


--
-- Name: stock_minus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stock_minus_id_seq', 149, true);


--
-- Name: stock_plus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stock_plus_id_seq', 28, true);


--
-- Name: act act_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.act
    ADD CONSTRAINT act_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: log log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: stock_minus stock_minus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_minus
    ADD CONSTRAINT stock_minus_pkey PRIMARY KEY (id);


--
-- Name: stock_plus stock_plus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_plus
    ADD CONSTRAINT stock_plus_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

