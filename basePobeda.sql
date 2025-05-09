PGDMP  '    ,                }            Pobeda    17.4    17.4 9    d           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            e           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            f           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            g           1262    16520    Pobeda    DATABASE     n   CREATE DATABASE "Pobeda" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
    DROP DATABASE "Pobeda";
                     postgres    false            �            1259    16522    aerich    TABLE     �   CREATE TABLE public.aerich (
    id integer NOT NULL,
    version character varying(255) NOT NULL,
    app character varying(100) NOT NULL,
    content jsonb NOT NULL
);
    DROP TABLE public.aerich;
       public         heap r       postgres    false            �            1259    16521    aerich_id_seq    SEQUENCE     �   CREATE SEQUENCE public.aerich_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.aerich_id_seq;
       public               postgres    false    218            h           0    0    aerich_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.aerich_id_seq OWNED BY public.aerich.id;
          public               postgres    false    217            �            1259    16588    classes    TABLE     1  CREATE TABLE public.classes (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    state_game boolean DEFAULT false NOT NULL,
    last_task_number integer DEFAULT 1 NOT NULL,
    start_time timestamp with time zone,
    is_active boolean DEFAULT true NOT NULL,
    last_task_id bigint
);
    DROP TABLE public.classes;
       public         heap r       postgres    false            �            1259    16587    classes_id_seq    SEQUENCE     w   CREATE SEQUENCE public.classes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.classes_id_seq;
       public               postgres    false    220            i           0    0    classes_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.classes_id_seq OWNED BY public.classes.id;
          public               postgres    false    219            �            1259    16630    options    TABLE     �   CREATE TABLE public.options (
    id integer NOT NULL,
    options character varying(255) NOT NULL,
    option_text text NOT NULL,
    question_id bigint NOT NULL
);
    DROP TABLE public.options;
       public         heap r       postgres    false            �            1259    16629    options_id_seq    SEQUENCE     �   CREATE SEQUENCE public.options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.options_id_seq;
       public               postgres    false    226            j           0    0    options_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.options_id_seq OWNED BY public.options.id;
          public               postgres    false    225            �            1259    16600 	   questions    TABLE     ;  CREATE TABLE public.questions (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    data text,
    grade_group character varying(25) NOT NULL,
    text text NOT NULL,
    correct_answer text NOT NULL,
    answer_type character varying(255) NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);
    DROP TABLE public.questions;
       public         heap r       postgres    false            �            1259    16599    questions_id_seq    SEQUENCE     y   CREATE SEQUENCE public.questions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.questions_id_seq;
       public               postgres    false    222            k           0    0    questions_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;
          public               postgres    false    221            �            1259    16644    scores    TABLE     �   CREATE TABLE public.scores (
    id bigint NOT NULL,
    score integer DEFAULT 0 NOT NULL,
    class__id bigint NOT NULL,
    quest_id bigint NOT NULL,
    user_id bigint
);
    DROP TABLE public.scores;
       public         heap r       postgres    false            �            1259    16643    scores_id_seq    SEQUENCE     v   CREATE SEQUENCE public.scores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.scores_id_seq;
       public               postgres    false    228            l           0    0    scores_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.scores_id_seq OWNED BY public.scores.id;
          public               postgres    false    227            �            1259    16612    users    TABLE     �   CREATE TABLE public.users (
    id bigint NOT NULL,
    tg_username character varying(255),
    tg_id bigint NOT NULL,
    full_name character varying(255),
    sch_class_id bigint NOT NULL
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    16611    users_id_seq    SEQUENCE     u   CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               postgres    false    224            m           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               postgres    false    223            �           2604    16525 	   aerich id    DEFAULT     f   ALTER TABLE ONLY public.aerich ALTER COLUMN id SET DEFAULT nextval('public.aerich_id_seq'::regclass);
 8   ALTER TABLE public.aerich ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    217    218    218            �           2604    16591 
   classes id    DEFAULT     h   ALTER TABLE ONLY public.classes ALTER COLUMN id SET DEFAULT nextval('public.classes_id_seq'::regclass);
 9   ALTER TABLE public.classes ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219    220            �           2604    16633 
   options id    DEFAULT     h   ALTER TABLE ONLY public.options ALTER COLUMN id SET DEFAULT nextval('public.options_id_seq'::regclass);
 9   ALTER TABLE public.options ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    225    226    226            �           2604    16603    questions id    DEFAULT     l   ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);
 ;   ALTER TABLE public.questions ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    221    222    222            �           2604    16647 	   scores id    DEFAULT     f   ALTER TABLE ONLY public.scores ALTER COLUMN id SET DEFAULT nextval('public.scores_id_seq'::regclass);
 8   ALTER TABLE public.scores ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    227    228    228            �           2604    16615    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    223    224    224            W          0    16522    aerich 
   TABLE DATA           ;   COPY public.aerich (id, version, app, content) FROM stdin;
    public               postgres    false    218   �A       Y          0    16588    classes 
   TABLE DATA           n   COPY public.classes (id, name, state_game, last_task_number, start_time, is_active, last_task_id) FROM stdin;
    public               postgres    false    220   J       _          0    16630    options 
   TABLE DATA           H   COPY public.options (id, options, option_text, question_id) FROM stdin;
    public               postgres    false    226   kJ       [          0    16600 	   questions 
   TABLE DATA           n   COPY public.questions (id, name, data, grade_group, text, correct_answer, answer_type, is_active) FROM stdin;
    public               postgres    false    222   �O       a          0    16644    scores 
   TABLE DATA           I   COPY public.scores (id, score, class__id, quest_id, user_id) FROM stdin;
    public               postgres    false    228   AY       ]          0    16612    users 
   TABLE DATA           P   COPY public.users (id, tg_username, tg_id, full_name, sch_class_id) FROM stdin;
    public               postgres    false    224   ^Y       n           0    0    aerich_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.aerich_id_seq', 5, true);
          public               postgres    false    217            o           0    0    classes_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.classes_id_seq', 8, true);
          public               postgres    false    219            p           0    0    options_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.options_id_seq', 120, true);
          public               postgres    false    225            q           0    0    questions_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.questions_id_seq', 53, true);
          public               postgres    false    221            r           0    0    scores_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.scores_id_seq', 1, false);
          public               postgres    false    227            s           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 1, false);
          public               postgres    false    223            �           2606    16529    aerich aerich_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.aerich
    ADD CONSTRAINT aerich_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.aerich DROP CONSTRAINT aerich_pkey;
       public                 postgres    false    218            �           2606    16598    classes classes_name_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.classes
    ADD CONSTRAINT classes_name_key UNIQUE (name);
 B   ALTER TABLE ONLY public.classes DROP CONSTRAINT classes_name_key;
       public                 postgres    false    220            �           2606    16596    classes classes_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.classes
    ADD CONSTRAINT classes_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.classes DROP CONSTRAINT classes_pkey;
       public                 postgres    false    220            �           2606    16637    options options_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.options DROP CONSTRAINT options_pkey;
       public                 postgres    false    226            �           2606    16610    questions questions_name_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_name_key UNIQUE (name);
 F   ALTER TABLE ONLY public.questions DROP CONSTRAINT questions_name_key;
       public                 postgres    false    222            �           2606    16608    questions questions_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.questions DROP CONSTRAINT questions_pkey;
       public                 postgres    false    222            �           2606    16650    scores scores_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.scores DROP CONSTRAINT scores_pkey;
       public                 postgres    false    228            �           2606    16619    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    224            �           2606    16623    users users_tg_id_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_tg_id_key UNIQUE (tg_id);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_tg_id_key;
       public                 postgres    false    224            �           2606    16621    users users_tg_username_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_tg_username_key UNIQUE (tg_username);
 E   ALTER TABLE ONLY public.users DROP CONSTRAINT users_tg_username_key;
       public                 postgres    false    224            �           2606    16666 $   classes fk_classes_question_392d0726    FK CONSTRAINT     �   ALTER TABLE ONLY public.classes
    ADD CONSTRAINT fk_classes_question_392d0726 FOREIGN KEY (last_task_id) REFERENCES public.questions(id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.classes DROP CONSTRAINT fk_classes_question_392d0726;
       public               postgres    false    222    220    4787            �           2606    16677 $   options fk_options_question_b9b48a10    FK CONSTRAINT     �   ALTER TABLE ONLY public.options
    ADD CONSTRAINT fk_options_question_b9b48a10 FOREIGN KEY (question_id) REFERENCES public.questions(id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.options DROP CONSTRAINT fk_options_question_b9b48a10;
       public               postgres    false    4787    226    222            �           2606    16638 #   options options_question_id_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_question_id_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id) ON DELETE CASCADE;
 M   ALTER TABLE ONLY public.options DROP CONSTRAINT options_question_id_id_fkey;
       public               postgres    false    4787    226    222            �           2606    16651    scores scores_class__id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_class__id_fkey FOREIGN KEY (class__id) REFERENCES public.classes(id) ON DELETE CASCADE;
 F   ALTER TABLE ONLY public.scores DROP CONSTRAINT scores_class__id_fkey;
       public               postgres    false    228    220    4783            �           2606    16656    scores scores_quest_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_quest_id_fkey FOREIGN KEY (quest_id) REFERENCES public.questions(id) ON DELETE RESTRICT;
 E   ALTER TABLE ONLY public.scores DROP CONSTRAINT scores_quest_id_fkey;
       public               postgres    false    222    228    4787            �           2606    16661    scores scores_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.scores DROP CONSTRAINT scores_user_id_fkey;
       public               postgres    false    4789    228    224            �           2606    16624    users users_sch_class_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_sch_class_id_fkey FOREIGN KEY (sch_class_id) REFERENCES public.classes(id) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.users DROP CONSTRAINT users_sch_class_id_fkey;
       public               postgres    false    224    4783    220            W   -  x��\[o�H~&�"⩕�RҾ���l�M�n�ne9��X56���Q��_�9����ԇ��}f|�����֐���i��l6Z���=�>�&�Jt�����q�%���������)�q�~tX7�		F�[�*�������"6�����olj�
e�oe�&lh�C�Ո�:sy�5�?<3���M��U%��L�3]����||���z#)�>�]�T�24cP�X2�rV%�ǩ���A�9�dW�௡�vV=�w��<iw�g�W�3v���3wVo+�6��i�N�i��0�uw�������|��nl�Y=iNb#fӌ��2�CC����o������ݲmB���xt3.�dk�nL�_�N�1���<=M�{Fd���^]|�^�`_:�0� 1jA�`&�4�2��3�-�W��`T�|*f�y=�cVR�|6��o��УC]��������۾������e��K~�dz�զ��O�s>45m:�*�s�����rY���;by�����x�-UZR������������O�ٔ)��t|��ٶ�ư٘��RV�\o7���V������霞5|�|)'Sr�ϭID�����r')�l�y~�ɾ_��L�uu]������Wa��h��=���;�"���H��͑�dPɾ�X∑Gi!$��֙�%��8?�
��LX�c�+`���|ҩ�TJ���Q���0���J#�+ �q}T�+�c_��<����O�����ws��!ptv�Ǌ��s1�+��JJ���J��V�I�#S�ӈ����$�02��u8����1�|�<��	�M]c�������1�ܸ��枤b�IR�W��ZD4-�~ZzG�QS2̇�>Ot�T�|ˮrY�U]�9�����H�U5*�x:�_��G�˿"R��;��+Mg�16��U,�9��?�p�~z���kl#5[bvU��m��!2AuL>NV�/~��y�1�/����e��LgKxɭ��N��3b�z'ӽ3�d���N��p33lU��Lν���T\�_k%:��z_F�|�i8x��?���sl�*s�-sV��Wl��e0o\�B��.�W�}AŴ,�PI6쇭�M����,��c������05�6D�6z�(y8%��'�J�P��iT��Uk�K��(y��J�P�T.���<J�P�$�\�}g+�E�0l�`�rw�_,�qj�J��<���k[���H���7����G��8z8�D�*�P1��9T�UX�����S J
9�sU�6�oai����Y \q��p0�ԧ�>u�V�eH|kZ�~�˫��BbT�n`
�{Q�[EDu/�{�45Ȍ��{nE�Ǧ@f$]fdw�b�Gś=����S?z�Zj`�܅<QNe.�$Y:?Kd ER�ɽ���6��w=��_��$��D��8��q�1�֥��ŉ�W����L��=/׶f�3%�lOGo`u#��F�=cS�j��WSH��`_<�0������#C����4D}_���^����W��&zz���iT���he�+�i�%�|���@��@��`6cΞp��ph�"%`2���aI����u�F*�T 6�>�f/b�EđY���Ѯ�B���k o�`��7 �Q��<�7 �!�\�]S� o���}�!�7�e����x#m��7 �����
���B ��ۆ
 o$��QŹ�M�!��Bb o<w�7 ������ �"3���dF �� ����fI �Qv��M���]� ��ѫ ���r��B��	}o ol& �!TZ� ��4 ������{A�1\!R/��+ 7 �!�9vA�;k�6��j����v ��i�� ��a��J ���Xw�m�  ����2�:*�m l���
���"�m�`i�k ����lU0 �<�� M ib�V�Q<��X	�;|V���Py+X	;l�ď&�'1M�h�G����M�h�G?���ď&~4�W��h�� M��o�����ʷ��M������_�&��4��i%=`E�õ��������      Y   D   x�3�4�0�3�Ӏ3Ə�Hpq���s���� E&���rZ��1�D1�44@��44D����� �$K      _   *  x��V�r#E}���~�*���G.����	lB%��C[�eC����/d��/�����vB��ĭ�ԒΑ4I�e��p&��(qi�UTo�Y�u�f��.,´=���<����ԇ�}V��.�:�(���ǿ�a�(u%܆s�.�
��p ���o�C\4�.4>L�wK-�Tx�:��7���h-�C�d.���]��n՞Q�����gL����^�Y{��'|�Ҍ��L�"���$�G%�BFH�7��3�{͂/�
�%C�HK�5�t#���a��.��ҕ�Ծ�Hkz}�����,��s����$V��Q��TunOU�	��C��p��)o��=�Mn^�zѵ���h�u��-�����K��G�����7�tgH�j|lz�U��G��T.����/%B(��:�_�ށr[�,�vQ+���
�"�dB�,�����.������(�O��[���YG�MF��re�KQ.h��E`��t�%>����{ӣ�D�iӍ����Y��P��]!u�z��B��.D#Es��k@?d#�r��`�Z��@��P��:Z�Rx�T�0������n�"a��FB����i���xPLc�d�+ԈcB�'Vױ��+��9���lي�M��ʫJ�j��p���#�����F�Mӂ�7ϸ)Ōk��t#fW�m�KW���<�N	�j�1����@=�WC�bo4x�p�93��4ǸoO�ފ #�Z	8��'Ă;�3F��������i9�U;���b���i5��D/�kF��㚭,!�傉��Y>� /ō)��-�Px&�����k& �w�'��k�cV	ď]�|��W	���Q�v!���VW0��x������=J{��s����J �P��C�)���m<+�9P7q�^�n�pS��Mm����v�G�i}�Y,���3WǶ��}�{���iP�	'��Z�ֱf��![d�&�Ew��J��<�ݙy�j͏�E�U/,l��v�ۥ�z�z���B�30τY�𘵋��Օm�E��sz���d��O~�A�?����w�8��R9�-���#��k��D����b#���w��p�v�����a��8\|�?�1�o9��.���ۓk��0RW�*�D��ىT�)���������̍�
�s��{%�������\e'�7�ࣩ���B��_'���f���6�ѧ�no߅��(~�l5��!!���Df5N��۩�<;��gi��_FE�����W���>y'�����>�4G�ݠ�L��#��~�էV,}>B��/�s�i5      [   �	  x��YKoE>O~��H�����\|��"% 8p1�EB�8�K�y��1J���<��x����=�_B�W�==�]�	(�������WO�詧ѦDuդ�M�����+*�z�:ю
�����P��>𯬭�\�xrr��⭕�k�gVnM^[Y^]]_^Y؈-,,�(�\�vqa�P+,�o�V�k�k�KWW׮oܺ|eq}c��z}y}y�p������uZ�����}��|�5���IO=VՏ��j�j������ً.]����O��S5O�MBե�o}�2^痦JU{���u�{����Q���;�u�G��v��J�WmzȲ��)��Ο=G��=����~H	�]�^��뫀���G���QTEr���h`�ަ�m���Ӣ=�O��pbs88�<��<Z�+'T�,�<�˪}���߁�^��ӏ��omu❄��M&e�3�7HЏ6�|@Rh{�6�{V��U֞���C��f2龫:�F���Q��C��d���z$`����C�u;o��#���f�{-`��P��L�����1L҇��X����b��KY��������k�,���A��Q#6L�H�1E��j��yu�rtՄ�Yc��i��^p�0�b�O䑕L�!PȈ�9ڍq��>}t��� �l�J��� �3"n��̊����������ٺ�D����b�Z{�/��bD�,/���%�8$�ۙ@�k�2h�p~Fg�����f�� �N-%�s�}���#�-BZ*��>i����Q}?�S7��J ��DM�D���0"#NG�k�{E�{���ç��Vf��ɓ�$���Vt�rh����	�s�m")7x=�H����=�5����;@+lA>);��i�����RvL=��9M�aJ��]2��%	���AUez�ܓ�QT;�cL0����	�&o�[�\�3����FG �'�Ay�=݅�!�o�ş��BNZw��u����"�j�Δ8��	WF�f�K<��vl8�{�=`o��b�׹��R�U�z�9'\sT_��o���澮����5�R���J�ےD���b����:n��9�7?$h_zC�O}�97��YmP��K/��9�b�����r|�>����Bu��t�H+(If����%=X�� ���)����J`��6= ����+�U�4�
g�dW��# 6��N�A��zS@�?�����m��l�-���bI������VO�!�4�ms0�~)�"��Y�I٧Am��8�=Н�۴� �!�T��*פͮ���Ot�.��6��q��t>���Й����� ��:�k8��s�;2��7=9��T(���j.G���=)C=�������T ~���l �ɕ���CBC��6��׊qԥB��gb�4����C���h`�A�\�֩~�arN���]x�d�����B�
xY�jʟr4����F��̟ȫ�*���6��%�G�}��Ⱦ`��Aؗ?p�����W4AP�0i�}�#w(#w��N��LK'���D^SZMi�L���\*��o�7@D#v�*#֟|&�O�
0�lJ��)"ځ}��3όiO^J��ۋܞ��%ѥ	����'��X/��A��[{���Aܴ����8}ApLY�r\�O������MpK,�T���x�q܀���!f�8���w���Q��N)�Nq_���-��$��hBV;v�X� <������A�X� �bT���^�/�M��P~��h�
�2IK6�2�������r�=�Y��3�4��=�}�� '� ��+�[Y)zN��
��i��)v�ƭ���[2��{���4Kǫ��	���#��L�s�l��E:}�����IO�t�ۆ��������;MQ�-�49�N�P�~�8�t�rƜ&�p��؂�)0���=Ӹ%O�DR,�Tb��q�&��X��їA[2L�N���N�2;��*��4��d��-*abF�����;ic=���h��X�[�E'�@�q8��sc���?���ŬΩ���H��2�]�dI�A΅�"�XC�Ε�Iג��J�9#�=������T�g��!{���_���� /klq�[:�],�������6�I�q��ޗ,���0�����:����]��BmS��G��?]���2o�} ��Xu�1ɞ�蛒��Y�P�ՕVa����;�V!!x�\c�`6"=ԏ-7o�q ͚���n#U��L����;����T�~6L;6�dz�j�T�w�<95�q>�m�&��L���rZ��-��-�n�}|��M��1�U��>�z?+�O�μ!m�i���\M���LΛ�{�נ�7IՒ���r�ܴ���0�moum~���I$i�E_X�Y�Y��p��$0[F��Nv�z�}y��Y�^�=~u3����sh�C�`4�oΜ:u�_�f��      a      x������ � �      ]      x������ � �     