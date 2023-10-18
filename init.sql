--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Debian 16.0-1.pgdg120+1)
-- Dumped by pg_dump version 16.0 (Debian 16.0-1.pgdg120+1)

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
-- Name: category; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.category (
    id integer NOT NULL,
    title text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    clues_count integer
);


ALTER TABLE public.category OWNER TO myuser;

--
-- Name: jservice_pk_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.jservice_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jservice_pk_seq OWNER TO myuser;

--
-- Name: jservice; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.jservice (
    jservice_pk integer DEFAULT nextval('public.jservice_pk_seq'::regclass) NOT NULL,
    id integer NOT NULL,
    answer text,
    question text,
    value integer,
    airdate timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    category_id integer,
    game_id integer,
    invalid_count integer
);


ALTER TABLE public.jservice OWNER TO myuser;

--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.category (id, title, created_at, updated_at, clues_count) FROM stdin;
\.


--
-- Data for Name: jservice; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.jservice (jservice_pk, id, answer, question, value, airdate, created_at, updated_at, category_id, game_id, invalid_count) FROM stdin;
\.


--
-- Name: jservice_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.jservice_pk_seq', 1, false);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: jservice jservice_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.jservice
    ADD CONSTRAINT jservice_pkey PRIMARY KEY (jservice_pk);


--
-- PostgreSQL database dump complete
--

