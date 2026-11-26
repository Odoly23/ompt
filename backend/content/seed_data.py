"""Initial content for the OPMT website.

Sources:
- "Perfil OPMT no atividades_website.docx" and "ESTATUTOS DA OPMT.docx",
  sent by Filomena de Almeida (OPMT) on 17 Oct 2025.
- Exhibition poster "Buibere Hamrik Tuba Rai Metin Ukun Rasik An" (OPMT, 2016).

Anything marked sample=True is placeholder content that OPMT must confirm or replace.
Each translated value is a dict with tet / pt / id / en.
"""

SITE = {
    "name": "Organização Popular da Mulher Timor",
    "short_name": "OPMT",
    "founded": "1975-08-28",
    "address": "Sede Nasionál, Díli, Timor-Leste",
    "tagline": {
        "tet": "Organizasaun pioneira ba movimentu emansipasaun feto Timor-Leste",
        "pt": "Organização pioneira do movimento de emancipação da mulher timorense",
        "id": "Organisasi perintis gerakan emansipasi perempuan Timor-Leste",
        "en": "The pioneering organisation of the women's emancipation movement in Timor-Leste",
    },
    "about": {
        "tet": (
            "Organização Popular da Mulher Timor (OPMT) harii iha 28 agostu 1975 husi FRETILIN "
            "nu'udar ninia organizasaun massas, atu ajuda mobiliza no halo konxiensializasaun "
            "polítika ba populasaun tomak atu partisipa iha misaun liberta Pátria no Povu.\n\n"
            "Liuhusi partisipasaun iha luta koletiva, Buibere ida-idak liberta-an nu'udar feto "
            "matenek ho kbiit rasik no sai parseira válida mane sira nian iha luta libertasaun "
            "nasionál no iha Timor-Leste livre no independente. OPMT mós konxiensializa povu "
            "kona-ba FRETILIN ninia prinsípiu sira: igualdade direitu mane no feto, inkluzaun no "
            "justisa sosiál.\n\n"
            "Ohin loron OPMT nu'udar pesoa koletiva ho autonomia administrativa no patrimoniál, "
            "ho sede nasionál iha Díli, no estrutura iha suku, postu administrativu, munisípiu "
            "no RAEOA."
        ),
        "pt": (
            "A Organização Popular da Mulher Timor (OPMT) foi criada a 28 de Agosto de 1975 pela "
            "FRETILIN como sua organização de massas, para ajudar a mobilizar e consciencializar "
            "politicamente toda a população a participar na missão de libertar a Pátria e o Povo.\n\n"
            "Através da participação na luta colectiva, cada Buibere libertou-se como mulher "
            "consciente e com força própria, tornando-se parceira válida dos homens na luta de "
            "libertação nacional e num Timor-Leste livre e independente. A OPMT consciencializa "
            "também o povo sobre os princípios da FRETILIN: igualdade de direitos entre homens e "
            "mulheres, inclusão e justiça social.\n\n"
            "Hoje a OPMT é uma pessoa colectiva com autonomia administrativa e patrimonial, com "
            "sede nacional em Díli e estruturas nos sucos, postos administrativos, municípios e "
            "na RAEOA."
        ),
        "id": (
            "Organização Popular da Mulher Timor (OPMT) didirikan pada 28 Agustus 1975 oleh FRETILIN "
            "sebagai organisasi massanya, untuk membantu memobilisasi dan menyadarkan seluruh rakyat "
            "secara politik agar ikut dalam misi membebaskan Tanah Air dan Rakyat.\n\n"
            "Melalui keterlibatan dalam perjuangan bersama, setiap Buibere membebaskan dirinya sebagai "
            "perempuan yang sadar dan berdaya, menjadi mitra sejajar laki-laki dalam perjuangan "
            "pembebasan nasional dan dalam Timor-Leste yang merdeka. OPMT juga menyadarkan rakyat "
            "tentang prinsip-prinsip FRETILIN: kesetaraan hak laki-laki dan perempuan, inklusi, dan "
            "keadilan sosial.\n\n"
            "Kini OPMT adalah badan hukum dengan otonomi administratif dan keuangan, berkantor pusat "
            "di Díli, dengan struktur di suco, pos administratif, munisipiu, dan RAEOA."
        ),
        "en": (
            "The Organização Popular da Mulher Timor (OPMT) was founded on 28 August 1975 by FRETILIN "
            "as its mass organisation, to help mobilise the whole population and raise its political "
            "awareness so that everyone could take part in liberating the homeland and its people.\n\n"
            "By taking part in the collective struggle, each Buibere freed herself as an aware woman "
            "with her own strength, and became an equal partner to men in the national liberation "
            "struggle and in a free and independent Timor-Leste. OPMT also teaches FRETILIN's "
            "principles: equal rights for women and men, inclusion and social justice.\n\n"
            "Today OPMT is a legal entity with administrative and financial autonomy. Its national "
            "office is in Díli, with structures in villages, administrative posts, municipalities "
            "and the RAEOA special region."
        ),
    },
    "mission": {
        "tet": (
            "Emansipasaun feto, hasai prekonseitu no diskriminasaun bazeia ba seksu iha sosiedade "
            "Timor nian, no promove atividade sira ne'ebé garante partisipasaun feto iha "
            "dezenvolvimentu nasionál no hasa'e ninia estatutu sosiál."
        ),
        "pt": (
            "A emancipação da mulher, a eliminação dos preconceitos e da discriminação com base no "
            "sexo existentes na sociedade timorense, incentivando actividades que assegurem a "
            "participação da mulher no desenvolvimento nacional e a elevação do seu estatuto social."
        ),
        "id": (
            "Emansipasi perempuan, penghapusan prasangka dan diskriminasi berbasis jenis kelamin dalam "
            "masyarakat Timor, serta mendorong kegiatan yang menjamin partisipasi perempuan dalam "
            "pembangunan nasional dan peningkatan status sosialnya."
        ),
        "en": (
            "The emancipation of women and the elimination of sex-based prejudice and discrimination "
            "in Timorese society, by promoting activities that secure women's participation in "
            "national development and raise their social standing."
        ),
    },
}

OBJECTIVES = [
    {"kind": "specific", "text": {
        "tet": "Mobiliza no eduka komunidade — feto, mane, foin-sa'e no labarik — atu respeita no defende direitus umanus, liuliu direitu feto no labarik nian.",
        "pt": "Mobilizar e educar a comunidade — a mulher, o homem, os jovens e as crianças — para respeitar e defender os direitos humanos, em especial os da mulher e da criança.",
        "id": "Memobilisasi dan mendidik masyarakat — perempuan, laki-laki, pemuda, dan anak — untuk menghormati dan membela hak asasi manusia, khususnya hak perempuan dan anak.",
        "en": "Mobilise and educate the community — women, men, young people and children — to respect and defend human rights, especially the rights of women and children."}},
    {"kind": "specific", "text": {
        "tet": "Promove diálogu, respeitu no toleránsia iha família, no kultura dame, liberdade no armonia sosiál.",
        "pt": "Promover o diálogo, o respeito e a tolerância no seio da família, e uma cultura de paz, liberdade e harmonia social.",
        "id": "Mendorong dialog, rasa hormat, dan toleransi dalam keluarga, serta budaya damai, kebebasan, dan harmoni sosial.",
        "en": "Promote dialogue, respect and tolerance within the family, and a culture of peace, freedom and social harmony."}},
    {"kind": "specific", "text": {
        "tet": "Luta ba igualdade oportunidade feto nian iha polítika, edukasaun, formasaun profisionál, saúde, empregu no asesu ba kréditu.",
        "pt": "Lutar pela igualdade de oportunidades da mulher na política, educação, formação profissional, saúde, emprego e acesso ao crédito.",
        "id": "Memperjuangkan kesetaraan kesempatan bagi perempuan dalam politik, pendidikan, pelatihan kerja, kesehatan, pekerjaan, dan akses kredit.",
        "en": "Fight for equal opportunities for women in politics, education, vocational training, health, employment and access to credit."}},
    {"kind": "specific", "text": {
        "tet": "Luta atu Estadu garante saúde materno-infantil no edukasaun ho kualidade, liuliu ba feto no labarik ne'ebé presiza liu.",
        "pt": "Lutar para que o Estado garanta a saúde materno-infantil e uma educação de qualidade, em especial às mulheres e crianças mais carenciadas.",
        "id": "Memperjuangkan agar Negara menjamin kesehatan ibu dan anak serta pendidikan bermutu, terutama bagi perempuan dan anak yang paling membutuhkan.",
        "en": "Press the State to guarantee maternal and child health and quality education, especially for the women and children most in need."}},
    {"kind": "specific", "text": {
        "tet": "Luta atu feto rurál iha direitu ba rai no asesu direta ba kréditu bankáriu.",
        "pt": "Lutar para que a mulher rural tenha direito à terra e acesso directo ao crédito bancário.",
        "id": "Memperjuangkan hak perempuan pedesaan atas tanah dan akses langsung ke kredit bank.",
        "en": "Fight for rural women's right to land and direct access to bank credit."}},
    {"kind": "specific", "text": {
        "tet": "Denunsia violénsia doméstika no forma hotu violénsia seksuál, tráfiku no esplorasaun hasoru feto no labarik, no apoia vítima sira.",
        "pt": "Denunciar a violência doméstica e todas as formas de violência sexual, tráfico e exploração contra a mulher e a criança, e apoiar as vítimas.",
        "id": "Mengecam kekerasan dalam rumah tangga serta segala bentuk kekerasan seksual, perdagangan orang, dan eksploitasi terhadap perempuan dan anak, serta mendampingi korban.",
        "en": "Speak out against domestic violence and every form of sexual violence, trafficking and exploitation of women and children, and support survivors."}},
    {"kind": "specific", "text": {
        "tet": "Dinamiza partisipasaun feto iha desportu, kultura no arte.",
        "pt": "Dinamizar a participação da mulher no desporto, na cultura e nas artes.",
        "id": "Menggerakkan partisipasi perempuan dalam olahraga, budaya, dan seni.",
        "en": "Increase women's participation in sport, culture and the arts."}},
    {"kind": "specific", "text": {
        "tet": "Haburas intersámbiu no fahe esperiénsia ho organizasaun feto seluk, bazeia ba solidariedade no ajuda malu.",
        "pt": "Fomentar o intercâmbio e a troca de experiências com outras organizações femininas, com base na solidariedade e entreajuda.",
        "id": "Mengembangkan pertukaran pengalaman dengan organisasi perempuan lain berdasarkan solidaritas dan saling membantu.",
        "en": "Build exchange and shared learning with other women's organisations, based on solidarity and mutual help."}},
]

HISTORY = [
    {"year": 1975, "date": "1975-08-28", "category": "foundation",
     "title": {"tet": "FRETILIN harii OPMT", "pt": "A FRETILIN cria a OPMT", "id": "FRETILIN mendirikan OPMT", "en": "FRETILIN founds OPMT"},
     "body": {
        "tet": "OPMT harii nu'udar organizasaun massas FRETILIN atu enkuadra feto sira no mobiliza povu ba luta libertasaun Pátria. Rosa Bonaparte Soares \"Muki\" sai Sekretária-Jeral dahuluk.",
        "pt": "A OPMT é criada como organização de massas da FRETILIN, para enquadrar as mulheres e mobilizar o povo na luta pela libertação da Pátria. Rosa Bonaparte Soares \"Muki\" é a primeira Secretária-Geral.",
        "id": "OPMT didirikan sebagai organisasi massa FRETILIN untuk menghimpun perempuan dan memobilisasi rakyat dalam perjuangan membebaskan Tanah Air. Rosa Bonaparte Soares \"Muki\" menjadi Sekretaris Jenderal pertama.",
        "en": "OPMT is created as FRETILIN's mass organisation, to organise women and mobilise the people in the struggle to free the homeland. Rosa Bonaparte Soares \"Muki\" becomes its first Secretary-General."}},
    {"year": 1975, "category": "foundation",
     "title": {"tet": "Programa dahuluk: krexe, alfabetizasaun no saúde", "pt": "Primeiros programas: creche, alfabetização e saúde", "id": "Program pertama: penitipan anak, pemberantasan buta huruf, dan kesehatan", "en": "First programmes: childcare, literacy and health"},
     "body": {
        "tet": "Atividade dahuluk OPMT iha agostu 1975 mak harii krexe atu tau matan ba oan kiak sira. Comissão Directiva dezenvolve programa edukasaun krexe, kampaña alfabetizasaun, produsaun, saúde no asisténsia, no habelar estrutura ba nível rejionál no sub-rejionál.",
        "pt": "A primeira actividade da OPMT, em Agosto de 1975, foi criar uma creche para cuidar dos órfãos. A Comissão Directiva desenvolveu programas de creche, campanha de alfabetização, produção, saúde e assistência, e alargou a estrutura aos níveis regional e sub-regional.",
        "id": "Kegiatan pertama OPMT pada Agustus 1975 adalah mendirikan tempat penitipan untuk merawat anak yatim. Comissão Directiva mengembangkan program penitipan anak, kampanye melek huruf, produksi, kesehatan, dan bantuan sosial, serta memperluas struktur ke tingkat regional dan sub-regional.",
        "en": "OPMT's first activity, in August 1975, was a crèche to care for orphans. The Comissão Directiva then ran programmes in childcare, literacy, production, health and welfare, and extended its structure to regional and sub-regional levels."}},
    {"year": 1975, "date": "1975-12-08", "category": "resistance",
     "title": {"tet": "Rosa \"Muki\" Bonaparte mate iha invazaun", "pt": "Rosa \"Muki\" Bonaparte morta na invasão", "id": "Rosa \"Muki\" Bonaparte gugur saat invasi", "en": "Rosa \"Muki\" Bonaparte killed in the invasion"},
     "body": {
        "tet": "Sekretária-Jeral dahuluk OPMT hetan kaptura no oho husi militár indonézia iha Ponte Cais, Díli, iha loron invazaun nian.",
        "pt": "A primeira Secretária-Geral da OPMT é capturada e morta por militares indonésios no Ponte Cais, em Díli, no dia da invasão.",
        "id": "Sekretaris Jenderal pertama OPMT ditangkap dan dibunuh oleh militer Indonesia di Ponte Cais, Díli, pada hari invasi.",
        "en": "OPMT's first Secretary-General is captured and killed by Indonesian soldiers at Ponte Cais, Díli, on the day of the invasion."}},
    {"year": 1976, "category": "resistance",
     "title": {"tet": "Programa kontinua iha Bases de Apoio", "pt": "Os programas continuam nas Bases de Apoio", "id": "Program berlanjut di Bases de Apoio", "en": "Programmes continue in the Bases de Apoio"},
     "body": {
        "tet": "Durante okupasaun indonézia, programa krexe, alfabetizasaun, produsaun, kulinária no konxiensializasaun polítika kontinua iha Bases de Apoio ho kontrolu husi FRETILIN no FALINTIL. Feto sira partisipa iha frente hotu: armada, klandestina no diplomátika.",
        "pt": "Durante a ocupação indonésia, os programas de creche, alfabetização, produção, culinária e consciencialização política continuam nas Bases de Apoio sob controlo da FRETILIN e das FALINTIL. As mulheres participam em todas as frentes: armada, clandestina e diplomática.",
        "id": "Selama pendudukan Indonesia, program penitipan anak, melek huruf, produksi, tata boga, dan penyadaran politik berlanjut di Bases de Apoio di bawah kendali FRETILIN dan FALINTIL. Perempuan ikut di semua front: bersenjata, klandestin, dan diplomatik.",
        "en": "During the Indonesian occupation, childcare, literacy, production, cooking and political education continued in the Bases de Apoio under FRETILIN and FALINTIL control. Women took part on every front: armed, clandestine and diplomatic."}},
    {"year": 1977, "category": "resistance",
     "title": {"tet": "Maria José Boavida \"Soimali\" lidera OPMT", "pt": "Maria José Boavida \"Soimali\" lidera a OPMT", "id": "Maria José Boavida \"Soimali\" memimpin OPMT", "en": "Maria José Boavida \"Soimali\" leads OPMT"},
     "body": {
        "tet": "Sekretária-Jeral daruak lidera OPMT iha ai-laran durante 1977–1979, to'o nia mate husi militár indonézia iha 1979.",
        "pt": "A segunda Secretária-Geral lidera a OPMT no mato entre 1977 e 1979, até ser morta por militares indonésios em 1979.",
        "id": "Sekretaris Jenderal kedua memimpin OPMT di hutan pada 1977–1979, hingga dibunuh militer Indonesia pada 1979.",
        "en": "The second Secretary-General leads OPMT in the mountains from 1977 to 1979, until she is killed by Indonesian soldiers in 1979."}},
    {"year": 1999, "category": "independence",
     "title": {"tet": "OPMT prezente iha Referendu", "pt": "A OPMT presente no Referendo", "id": "OPMT hadir dalam Referendum", "en": "OPMT at the Referendum"},
     "body": {
        "tet": "OPMT hatudu fali aten-barani no kapasidade organizasaun atu implementa orientasaun husi Komandu Superiór Luta nian iha Konsulta Populár.",
        "pt": "A OPMT demonstra, uma vez mais, coragem e capacidade de organização para levar a bom termo as orientações do Comando Superior da Luta na Consulta Popular.",
        "id": "OPMT sekali lagi menunjukkan keberanian dan kemampuan berorganisasi untuk menjalankan arahan Komando Tertinggi Perjuangan dalam Jajak Pendapat.",
        "en": "OPMT once again shows courage and organising ability in carrying out the guidance of the Supreme Command of the Struggle during the Popular Consultation."}},
    {"year": 2000, "date": "2000-03-11", "category": "organisation",
     "title": {"tet": "Ko-fundadora REDE FETO", "pt": "Co-fundadora da REDE FETO", "id": "Ikut mendirikan REDE FETO", "en": "Co-founder of REDE FETO"},
     "body": {
        "tet": "OPMT kontribui ba harii REDE FETO hamutuk ho FOKUPERS, GFFTL, GERTAK, ISMAIK, Asosiasaun Juristas, Feto Diáspora, OMT, AMST no organizasaun direitus umanus sira.",
        "pt": "A OPMT contribui para a criação da REDE FETO, com a FOKUPERS, GFFTL, GERTAK, ISMAIK, Associação de Juristas, Mulheres da Diáspora, OMT, AMST e organizações de direitos humanos.",
        "id": "OPMT ikut mendirikan REDE FETO bersama FOKUPERS, GFFTL, GERTAK, ISMAIK, Asosiasi Juris, Perempuan Diaspora, OMT, AMST, dan organisasi hak asasi manusia.",
        "en": "OPMT helps found REDE FETO with FOKUPERS, GFFTL, GERTAK, ISMAIK, the Jurists' Association, Diaspora Women, OMT, AMST and human rights organisations."}},
    {"year": 2000, "category": "organisation",
     "title": {"tet": "Mini-konferénsia no reorganizasaun", "pt": "Mini-conferência e reorganização", "id": "Mini-konferensi dan reorganisasi", "en": "Mini-conference and reorganisation"},
     "body": {
        "tet": "OPMT halo mini-konferénsia dahuluk ho kuadru antigu husi munisípiu sanulu-resin-tolu, no adota estatutu dahuluk ho karákter esperimentál. Regina Ximenes sai Sekretária-Jeral (2000–2006).",
        "pt": "A OPMT realiza a primeira mini-conferência com antigos quadros dos treze municípios e adopta, a título experimental, o primeiro Estatuto. Regina Ximenes é Secretária-Geral (2000–2006).",
        "id": "OPMT mengadakan mini-konferensi pertama dengan kader lama dari tiga belas munisipiu dan menetapkan statuta pertama secara uji coba. Regina Ximenes menjadi Sekretaris Jenderal (2000–2006).",
        "en": "OPMT holds its first mini-conference with former cadres from all thirteen municipalities and adopts a provisional first statute. Regina Ximenes becomes Secretary-General (2000–2006)."}},
    {"year": 2000, "category": "achievement",
     "title": {"tet": "Kongresu Nasionál Feto no Konstituisaun", "pt": "Congresso Nacional da Mulher e a Constituição", "id": "Kongres Nasional Perempuan dan Konstitusi", "en": "National Women's Congress and the Constitution"},
     "body": {
        "tet": "Hamutuk ho REDE FETO, OPMT organiza, lidera no fasilita Kongresu Nasionál Feto Timor-Leste, ne'ebé fó rekomendasaun ba artigu lubuk ida iha Konstituisaun RDTL kona-ba igualdade jéneru.",
        "pt": "Com a REDE FETO, a OPMT organiza, lidera e facilita o Congresso Nacional da Mulher de Timor-Leste, que recomenda vários artigos sobre igualdade de género para a Constituição da RDTL.",
        "id": "Bersama REDE FETO, OPMT menyelenggarakan, memimpin, dan memfasilitasi Kongres Nasional Perempuan Timor-Leste yang merekomendasikan sejumlah pasal kesetaraan gender untuk Konstitusi RDTL.",
        "en": "With REDE FETO, OPMT organises, leads and facilitates the National Women's Congress of Timor-Leste, which recommends several gender-equality articles for the RDTL Constitution."}},
    {"year": 2001, "category": "independence",
     "title": {"tet": "Buibere 11 iha Asembleia Konstituinte", "pt": "11 Buibere na Assembleia Constituinte", "id": "11 Buibere di Majelis Konstituante", "en": "11 Buibere in the Constituent Assembly"},
     "body": {
        "tet": "Membru OPMT na'in-sanulu-resin-ida tama iha Asembleia Konstituinte no kolabora iha elaborasaun Konstituisaun RDTL.",
        "pt": "Onze membros da OPMT integram a Assembleia Constituinte e colaboram na elaboração da Constituição da RDTL.",
        "id": "Sebelas anggota OPMT duduk di Majelis Konstituante dan ikut menyusun Konstitusi RDTL.",
        "en": "Eleven OPMT members sit in the Constituent Assembly and help draft the RDTL Constitution."}},
    {"year": 2006, "category": "organisation",
     "title": {"tet": "I Konferénsia Nasionál", "pt": "I Conferência Nacional", "id": "Konferensi Nasional I", "en": "1st National Conference"},
     "body": {
        "tet": "Konferénsia Nasionál aprova estatutu OPMT no hili Maria Lourdes Assunção Alves \"Merita\" nu'udar Sekretária-Jeral (2006–2011).",
        "pt": "A Conferência Nacional aprova o Estatuto da OPMT e elege Maria Lourdes Assunção Alves \"Merita\" Secretária-Geral (2006–2011).",
        "id": "Konferensi Nasional mengesahkan statuta OPMT dan memilih Maria Lourdes Assunção Alves \"Merita\" sebagai Sekretaris Jenderal (2006–2011).",
        "en": "The National Conference approves the OPMT statute and elects Maria Lourdes Assunção Alves \"Merita\" Secretary-General (2006–2011)."}},
    {"year": 2011, "category": "organisation",
     "title": {"tet": "II Konferénsia Nasionál", "pt": "II Conferência Nacional", "id": "Konferensi Nasional II", "en": "2nd National Conference"},
     "body": {
        "tet": "Merita eleita fali ba mandatu 2011–2016.",
        "pt": "Merita é reeleita para o mandato 2011–2016.",
        "id": "Merita terpilih kembali untuk masa jabatan 2011–2016.",
        "en": "Merita is re-elected for 2011–2016."}},
    {"year": 2016, "category": "organisation",
     "title": {"tet": "III Konferénsia Nasionál no estatutu foun", "pt": "III Conferência Nacional e novo Estatuto", "id": "Konferensi Nasional III dan statuta baru", "en": "3rd National Conference and new statute"},
     "body": {
        "tet": "OPMT aprova estatutu foun no Merita eleita ba mandatu datoluk (2016–2022). Iha tinan ne'e OPMT mós prepara espozisaun \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\".",
        "pt": "A OPMT aprova o novo Estatuto e Merita é eleita para um terceiro mandato (2016–2022). No mesmo ano a OPMT prepara a exposição \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\".",
        "id": "OPMT mengesahkan statuta baru dan Merita terpilih untuk periode ketiga (2016–2022). Pada tahun yang sama OPMT menyiapkan pameran \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\".",
        "en": "OPMT approves a new statute and Merita is elected for a third term (2016–2022). That year OPMT also prepares the exhibition \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\"."}},
    {"year": 2020, "date": "2020-06-10", "category": "achievement",
     "title": {"tet": "Lansamentu livru \"Buibere Hamriik Ukun Rasik An\"", "pt": "Lançamento do livro \"Buibere Hamriik Ukun Rasik An\"", "id": "Peluncuran buku \"Buibere Hamriik Ukun Rasik An\"", "en": "Launch of the book \"Buibere Hamriik Ukun Rasik An\""},
     "body": {
        "tet": "Livru husi Komisaun Peskiza no Hakerek OPMT kona-ba kontribuisaun feto sira ba luta libertasaun nasionál, lansa husi Prezidente Repúblika Francisco Guterres Lú Olo.",
        "pt": "O livro da Comissão de Pesquisa e Escrita da OPMT sobre a contribuição das mulheres para a luta de libertação nacional é lançado pelo Presidente da República Francisco Guterres Lú Olo.",
        "id": "Buku karya Komisi Riset dan Penulisan OPMT tentang kontribusi perempuan dalam perjuangan pembebasan nasional diluncurkan oleh Presiden Republik Francisco Guterres Lú Olo.",
        "en": "The book by OPMT's Research and Writing Commission on women's contribution to the national liberation struggle is launched by President Francisco Guterres Lú Olo."}},
    {"year": 2021, "date": "2021-05-24", "category": "organisation",
     "title": {"tet": "Omenajen ba Merita", "pt": "Homenagem a Merita", "id": "Penghormatan untuk Merita", "en": "Remembering Merita"},
     "body": {
        "tet": "Sekretária-Jeral Maria Lourdes Assunção Alves \"Merita\" mate tanba moras. Florentina Smith kaer knaar nu'udar Sekretária-Jeral interina.",
        "pt": "Falece, por doença, a Secretária-Geral Maria Lourdes Assunção Alves \"Merita\". Florentina Smith assume funções como Secretária-Geral interina.",
        "id": "Sekretaris Jenderal Maria Lourdes Assunção Alves \"Merita\" wafat karena sakit. Florentina Smith menjabat sebagai Sekretaris Jenderal sementara.",
        "en": "Secretary-General Maria Lourdes Assunção Alves \"Merita\" dies after an illness. Florentina Smith becomes interim Secretary-General."}},
    {"year": 2021, "category": "organisation",
     "title": {"tet": "IV Konferénsia Nasionál", "pt": "IV Conferência Nacional", "id": "Konferensi Nasional IV", "en": "4th National Conference"},
     "body": {
        "tet": "Konferénsia Nasionál aprova fali estatutu OPMT no hili Florentina Pereira da Conceição Martins Smith nu'udar Sekretária-Jeral ba mandatu 2022–2027.",
        "pt": "A Conferência Nacional reaprova o Estatuto da OPMT e elege Florentina Pereira da Conceição Martins Smith Secretária-Geral para o mandato 2022–2027.",
        "id": "Konferensi Nasional mengesahkan kembali statuta OPMT dan memilih Florentina Pereira da Conceição Martins Smith sebagai Sekretaris Jenderal periode 2022–2027.",
        "en": "The National Conference re-approves the OPMT statute and elects Florentina Pereira da Conceição Martins Smith Secretary-General for 2022–2027."}},
    {"year": 2022, "category": "achievement",
     "title": {"tet": "Prémio Liberdade de Expressão Max Stahl", "pt": "Prémio Liberdade de Expressão Max Stahl", "id": "Penghargaan Kebebasan Berekspresi Max Stahl", "en": "Max Stahl Freedom of Expression Prize"},
     "body": {
        "tet": "OPMT kompete ho kandidatu na'in-sia no manán prémiu husi Parlamentu Nasionál ho valór dólar rihun sanulu.",
        "pt": "A OPMT concorre com nove candidatos e vence o prémio do Parlamento Nacional, no valor de dez mil dólares.",
        "id": "OPMT bersaing dengan sembilan kandidat dan memenangkan penghargaan dari Parlemen Nasional senilai sepuluh ribu dolar.",
        "en": "Competing against nine candidates, OPMT wins the National Parliament's prize, worth ten thousand dollars."}},
    {"year": 2025, "date": "2025-08-22", "category": "organisation",
     "title": {"tet": "Omenajen ba Florentina Smith", "pt": "Homenagem a Florentina Smith", "id": "Penghormatan untuk Florentina Smith", "en": "Remembering Florentina Smith"},
     "body": {
        "tet": "Sekretária-Jeral Florentina Smith mate tanba moras. Tuir Estatutu Art. 23, Konsellu Koordenadór Nasionál hili adjunta ida atu kaer knaar interinu.",
        "pt": "Falece, por doença, a Secretária-Geral Florentina Smith. Nos termos do Art. 23.º do Estatuto, o Conselho Coordenador Nacional elege uma adjunta para assumir provisoriamente a função.",
        "id": "Sekretaris Jenderal Florentina Smith wafat karena sakit. Sesuai Pasal 23 Statuta, Dewan Koordinasi Nasional memilih seorang wakil untuk menjabat sementara.",
        "en": "Secretary-General Florentina Smith dies after an illness. Under Article 23 of the statute, the National Coordinating Council elects a deputy to serve in the interim."}},
    {"year": 2025, "date": "2025-09-13", "category": "achievement",
     "title": {"tet": "Selebrasaun tinan 50 OPMT", "pt": "Celebração dos 50 anos da OPMT", "id": "Perayaan 50 tahun OPMT", "en": "OPMT's 50th anniversary"},
     "body": {
        "tet": "OPMT selebra sinkuentenáriu iha sede CCF no fó-sai vídeu-dokumentáriu kona-ba ninia istória.",
        "pt": "A OPMT celebra o cinquentenário na sede do CCF e apresenta um vídeo-documentário sobre a sua história.",
        "id": "OPMT merayakan ulang tahun ke-50 di gedung CCF dan menayangkan video dokumenter tentang sejarahnya.",
        "en": "OPMT celebrates its 50th anniversary at the CCF and premieres a documentary video about its history."}},
]

FIGURES = [
    {"name": "Rosa Bonaparte Soares", "nickname": "Muki", "death_year": 1975, "is_heroine": True, "order": 1,
     "role": {"tet": "Sekretária-Jeral dahuluk OPMT, fundadora FRETILIN", "pt": "Primeira Secretária-Geral da OPMT, fundadora da FRETILIN", "id": "Sekretaris Jenderal pertama OPMT, pendiri FRETILIN", "en": "First Secretary-General of OPMT, FRETILIN founding member"},
     "bio": {
        "tet": "Membru fundadora FRETILIN no komité sentrál, lidera OPMT husi 28 agostu 1975. Iha 8 dezembru 1975 hetan kaptura no oho husi militár indonézia iha Ponte Cais, Díli.",
        "pt": "Membro fundador da FRETILIN e do seu comité central, liderou a OPMT desde 28 de Agosto de 1975. A 8 de Dezembro de 1975 foi capturada e morta por militares indonésios no Ponte Cais, em Díli.",
        "id": "Anggota pendiri FRETILIN dan komite sentralnya, memimpin OPMT sejak 28 Agustus 1975. Pada 8 Desember 1975 ia ditangkap dan dibunuh militer Indonesia di Ponte Cais, Díli.",
        "en": "A founding member of FRETILIN and its central committee, she led OPMT from 28 August 1975. On 8 December 1975 she was captured and killed by Indonesian soldiers at Ponte Cais, Díli."}},
    {"name": "Maria José Brites Boavida", "nickname": "Soimali", "death_year": 1979, "is_heroine": True, "order": 2,
     "role": {"tet": "Sekretária-Jeral daruak OPMT (1977–1979)", "pt": "Segunda Secretária-Geral da OPMT (1977–1979)", "id": "Sekretaris Jenderal kedua OPMT (1977–1979)", "en": "Second Secretary-General of OPMT (1977–1979)"},
     "bio": {
        "tet": "Lidera OPMT iha tempu rezisténsia iha ai-laran. Hetan oho husi militár indonézia iha 1979.",
        "pt": "Liderou a OPMT durante a resistência no mato. Foi morta por militares indonésios em 1979.",
        "id": "Memimpin OPMT selama perlawanan di hutan. Dibunuh militer Indonesia pada 1979.",
        "en": "Led OPMT during the resistance in the mountains. Killed by Indonesian soldiers in 1979."}},
    {"name": "Maria Tapó", "nickname": "", "is_heroine": True, "order": 3,
     "role": {"tet": "Feto dahuluk ne'ebé mate ho kilat iha liman", "pt": "Primeira mulher a morrer de arma na mão", "id": "Perempuan pertama yang gugur dengan senjata di tangan", "en": "The first woman to die with a weapon in her hands"},
     "bio": {
        "tet": "FRETILIN hili loron 3 novembru nu'udar Loron Feto atu fó omenajen ba Maria Tapó. OPMT kontribui ba rezolusaun ne'ebé konfirma 3 novembru nu'udar Loron Nasionál Feto.",
        "pt": "A FRETILIN escolheu o dia 3 de Novembro como Dia da Mulher em homenagem a Maria Tapó. A OPMT contribuiu para a resolução que confirmou o 3 de Novembro como Dia Nacional da Mulher.",
        "id": "FRETILIN menetapkan 3 November sebagai Hari Perempuan untuk menghormati Maria Tapó. OPMT ikut mendorong resolusi yang mengukuhkan 3 November sebagai Hari Perempuan Nasional.",
        "en": "FRETILIN chose 3 November as Women's Day in honour of Maria Tapó. OPMT helped secure the resolution confirming 3 November as National Women's Day."}},
    {"name": "Regina Ximenes", "nickname": "", "order": 4,
     "role": {"tet": "Sekretária-Jeral datoluk OPMT (2000–2006)", "pt": "Terceira Secretária-Geral da OPMT (2000–2006)", "id": "Sekretaris Jenderal ketiga OPMT (2000–2006)", "en": "Third Secretary-General of OPMT (2000–2006)"},
     "bio": {
        "tet": "Lidera OPMT iha tempu reorganizasaun hafoin Referendu.",
        "pt": "Liderou a OPMT no período de reorganização após o Referendo.",
        "id": "Memimpin OPMT pada masa reorganisasi setelah Referendum.",
        "en": "Led OPMT through its reorganisation after the Referendum."}},
    {"name": "Maria Lourdes Assunção Alves", "nickname": "Merita", "death_year": 2021, "order": 5,
     "role": {"tet": "Sekretária-Jeral OPMT (2006–2021)", "pt": "Secretária-Geral da OPMT (2006–2021)", "id": "Sekretaris Jenderal OPMT (2006–2021)", "en": "Secretary-General of OPMT (2006–2021)"},
     "bio": {
        "tet": "Eleita iha I, II no III Konferénsia Nasionál. Mate tanba moras iha 24 maiu 2021.",
        "pt": "Eleita na I, II e III Conferências Nacionais. Faleceu por doença a 24 de Maio de 2021.",
        "id": "Terpilih pada Konferensi Nasional I, II, dan III. Wafat karena sakit pada 24 Mei 2021.",
        "en": "Elected at the 1st, 2nd and 3rd National Conferences. Died after an illness on 24 May 2021."}},
    {"name": "Florentina Pereira da Conceição Martins Smith", "nickname": "", "death_year": 2025, "order": 6,
     "role": {"tet": "Sekretária-Jeral OPMT (2021–2025)", "pt": "Secretária-Geral da OPMT (2021–2025)", "id": "Sekretaris Jenderal OPMT (2021–2025)", "en": "Secretary-General of OPMT (2021–2025)"},
     "bio": {
        "tet": "Sekretária-Jeral interina hafoin Merita, depois eleita iha IV Konferénsia Nasionál ba 2022–2027. Mate tanba moras iha 22 agostu 2025.",
        "pt": "Secretária-Geral interina após Merita, depois eleita na IV Conferência Nacional para 2022–2027. Faleceu por doença a 22 de Agosto de 2025.",
        "id": "Sekretaris Jenderal sementara setelah Merita, kemudian terpilih pada Konferensi Nasional IV untuk 2022–2027. Wafat karena sakit pada 22 Agustus 2025.",
        "en": "Interim Secretary-General after Merita, then elected at the 4th National Conference for 2022–2027. Died after an illness on 22 August 2025."}},
]

MANDATES = [
    {"number": 1, "name": "Rosa Bonaparte Soares", "nickname": "Muki", "start_year": 1975, "end_year": 1975, "figure": "Rosa Bonaparte Soares",
     "note": {"tet": "28 agostu – 8 dezembru 1975. Oho husi militár indonézia iha Ponte Cais, Díli.", "pt": "28 de Agosto – 8 de Dezembro de 1975. Morta por militares indonésios no Ponte Cais, Díli.", "id": "28 Agustus – 8 Desember 1975. Dibunuh militer Indonesia di Ponte Cais, Díli.", "en": "28 August – 8 December 1975. Killed by Indonesian soldiers at Ponte Cais, Díli."}},
    {"number": 2, "name": "Maria José Brites Boavida", "nickname": "Soimali", "start_year": 1977, "end_year": 1979, "figure": "Maria José Brites Boavida",
     "note": {"tet": "Oho husi militár indonézia iha 1979.", "pt": "Morta por militares indonésios em 1979.", "id": "Dibunuh militer Indonesia pada 1979.", "en": "Killed by Indonesian soldiers in 1979."}},
    {"number": 3, "name": "Regina Ximenes", "start_year": 2000, "end_year": 2006, "figure": "Regina Ximenes",
     "note": {"tet": "Reorganizasaun OPMT hafoin Referendu.", "pt": "Reorganização da OPMT após o Referendo.", "id": "Reorganisasi OPMT setelah Referendum.", "en": "Reorganised OPMT after the Referendum."}},
    {"number": 4, "name": "Maria Lourdes Assunção Alves", "nickname": "Merita", "start_year": 2006, "end_year": 2011, "figure": "Maria Lourdes Assunção Alves",
     "note": {"tet": "Eleita iha I Konferénsia Nasionál.", "pt": "Eleita na I Conferência Nacional.", "id": "Terpilih pada Konferensi Nasional I.", "en": "Elected at the 1st National Conference."}},
    {"number": 5, "name": "Maria Lourdes Assunção Alves", "nickname": "Merita", "start_year": 2011, "end_year": 2016, "figure": "Maria Lourdes Assunção Alves",
     "note": {"tet": "Eleita iha II Konferénsia Nasionál.", "pt": "Eleita na II Conferência Nacional.", "id": "Terpilih pada Konferensi Nasional II.", "en": "Elected at the 2nd National Conference."}},
    {"number": 6, "name": "Maria Lourdes Assunção Alves", "nickname": "Merita", "start_year": 2016, "end_year": 2021, "figure": "Maria Lourdes Assunção Alves",
     "note": {"tet": "Eleita iha III Konferénsia Nasionál ba 2016–2022. Mate iha 24 maiu 2021; Florentina Smith sai interina.", "pt": "Eleita na III Conferência Nacional para 2016–2022. Faleceu a 24 de Maio de 2021; Florentina Smith assume interinamente.", "id": "Terpilih pada Konferensi Nasional III untuk 2016–2022. Wafat 24 Mei 2021; Florentina Smith menjabat sementara.", "en": "Elected at the 3rd National Conference for 2016–2022. Died 24 May 2021; Florentina Smith served as interim."}},
    {"number": 7, "name": "Florentina Pereira da Conceição Martins Smith", "start_year": 2022, "end_year": 2025, "figure": "Florentina Pereira da Conceição Martins Smith",
     "note": {"tet": "Eleita iha IV Konferénsia Nasionál ba 2022–2027. Mandatu hakotu iha 22 agostu 2025.", "pt": "Eleita na IV Conferência Nacional para 2022–2027. Mandato terminou a 22 de Agosto de 2025.", "id": "Terpilih pada Konferensi Nasional IV untuk 2022–2027. Masa jabatan berakhir 22 Agustus 2025.", "en": "Elected at the 4th National Conference for 2022–2027. Term ended on 22 August 2025."}},
]

ORGANS = [
    {"code": "conferencia-nacional", "order": 1,
     "name": {"tet": "Konferénsia Nasionál", "pt": "Conferência Nacional", "id": "Konferensi Nasional", "en": "National Conference"},
     "description": {
        "tet": "Órgaun aas liu OPMT. Aprova no altera estatutu, aprova programa kinkenál, hili Sekretária-Jeral no membru órgaun nasionál sira. Halibur kada tinan lima.",
        "pt": "Órgão máximo da OPMT. Aprova e altera os estatutos, aprova o programa quinquenal e elege a Secretária-Geral e os membros dos órgãos nacionais. Reúne de cinco em cinco anos.",
        "id": "Organ tertinggi OPMT. Mengesahkan dan mengubah statuta, menyetujui program lima tahunan, serta memilih Sekretaris Jenderal dan anggota organ nasional. Bersidang setiap lima tahun.",
        "en": "OPMT's highest body. It approves and amends the statute, adopts the five-year programme and elects the Secretary-General and members of the national bodies. Meets every five years."}},
    {"code": "conselho-coordenador", "order": 2,
     "name": {"tet": "Konsellu Koordenadór Nasionál", "pt": "Conselho Coordenador Nacional", "id": "Dewan Koordinasi Nasional", "en": "National Coordinating Council"},
     "description": {
        "tet": "Órgaun deliberativu aas liu entre Konferénsia sira. Prezide husi Sekretária-Jeral; inklui koordenadora munisipál sira no membru efetivu 25. Halibur dala ida kada tinan.",
        "pt": "Órgão deliberativo máximo entre Conferências. Presidido pela Secretária-Geral; integra as coordenadoras municipais e 25 membros efectivos. Reúne uma vez por ano.",
        "id": "Organ musyawarah tertinggi di antara Konferensi. Dipimpin Sekretaris Jenderal; beranggotakan koordinator munisipiu dan 25 anggota tetap. Bersidang sekali setahun.",
        "en": "The highest decision-making body between Conferences. Chaired by the Secretary-General; includes the municipal coordinators and 25 elected members. Meets once a year."}},
    {"code": "secretaria-geral", "order": 3,
     "name": {"tet": "Sekretária-Jeral", "pt": "Secretária-Geral", "id": "Sekretaris Jenderal", "en": "Secretary-General"},
     "description": {
        "tet": "Órgaun unipesoál ne'ebé asegura orientasaun polítika OPMT, reprezenta organizasaun iha nível nasionál no internasionál, no hetan ajuda husi adjunta sira.",
        "pt": "Órgão unipessoal que assegura a orientação política da OPMT e a representa a nível nacional e internacional, coadjuvada pelas adjuntas.",
        "id": "Organ perorangan yang menjamin arah politik OPMT dan mewakilinya di tingkat nasional dan internasional, dibantu para wakil.",
        "en": "A single-person office that sets OPMT's political direction and represents it nationally and internationally, supported by deputies."}},
    {"code": "jurisdicao", "order": 4,
     "name": {"tet": "Komisaun Jurisdisaun Nasionál", "pt": "Comissão de Jurisdição Nacional", "id": "Komisi Yurisdiksi Nasional", "en": "National Jurisdiction Commission"},
     "description": {
        "tet": "Órgaun dixiplina aas liu. Membru efetivu 5 no suplente 2, independente iha ninia julgamentu.",
        "pt": "O mais alto órgão de disciplina. Cinco membros efectivos e dois suplentes, independente nos seus julgamentos.",
        "id": "Organ disiplin tertinggi. Lima anggota tetap dan dua cadangan, independen dalam keputusannya.",
        "en": "The highest disciplinary body. Five members and two alternates, independent in its rulings."}},
    {"code": "fiscalizacao", "order": 5,
     "name": {"tet": "Komisaun Fiskalizasaun Nasionál", "pt": "Comissão de Fiscalização Nacional", "id": "Komisi Pengawasan Nasional", "en": "National Audit Commission"},
     "description": {
        "tet": "Fiskaliza jestaun finanseira no patrimóniu OPMT nian.",
        "pt": "Fiscaliza a gestão financeira e patrimonial da OPMT.",
        "id": "Mengawasi pengelolaan keuangan dan aset OPMT.",
        "en": "Oversees OPMT's finances and assets."}},
]

# Current leadership is not yet confirmed — placeholders only.
LEADERS = [
    {"organ": "secretaria-geral", "name": "Sei konfirma", "order": 1,
     "position": {"tet": "Sekretária-Jeral interina", "pt": "Secretária-Geral interina", "id": "Sekretaris Jenderal sementara", "en": "Interim Secretary-General"}},
    {"organ": "secretaria-geral", "name": "Sei konfirma", "order": 2,
     "position": {"tet": "Adjunta Sekretária-Jeral", "pt": "Adjunta da Secretária-Geral", "id": "Wakil Sekretaris Jenderal", "en": "Deputy Secretary-General"}},
    {"organ": "jurisdicao", "name": "Sei konfirma", "order": 3,
     "position": {"tet": "Sekretária Komisaun Jurisdisaun Nasionál", "pt": "Secretária da Comissão de Jurisdição Nacional", "id": "Sekretaris Komisi Yurisdiksi Nasional", "en": "Secretary, National Jurisdiction Commission"}},
    {"organ": "fiscalizacao", "name": "Sei konfirma", "order": 4,
     "position": {"tet": "Sekretária Komisaun Fiskalizasaun Nasionál", "pt": "Secretária da Comissão de Fiscalização Nacional", "id": "Sekretaris Komisi Pengawasan Nasional", "en": "Secretary, National Audit Commission"}},
]

MUNICIPALITIES = [
    ("Aileu", "aileu", -8.7281, 125.5664, False),
    ("Ainaro", "ainaro", -8.9925, 125.5083, False),
    ("Ataúro", "atauro", -8.2470, 125.5850, False),
    ("Baucau", "baucau", -8.4660, 126.4520, False),
    ("Bobonaro", "bobonaro", -8.9950, 125.2190, False),
    ("Covalima", "covalima", -9.3130, 125.2560, False),
    ("Díli", "dili", -8.5560, 125.5780, False),
    ("Ermera", "ermera", -8.7230, 125.4370, False),
    ("Lautém", "lautem", -8.5190, 127.0020, False),
    ("Liquiçá", "liquica", -8.5880, 125.3410, False),
    ("Manatuto", "manatuto", -8.5120, 126.0120, False),
    ("Manufahi", "manufahi", -9.0000, 125.6460, False),
    ("Viqueque", "viqueque", -8.8580, 126.3640, False),
    ("RAEOA (Oé-Cusse Ambeno)", "raeoa", -9.2000, 124.3800, True),
]

POSTS = {
    "dili": ["Cristo Rei", "Dom Aleixo", "Metinaro", "Nain Feto", "Vera Cruz"],
    "manufahi": ["Alas", "Fatuberliu", "Same", "Turiscai"],
    "baucau": ["Baguia", "Baucau", "Laga", "Quelicai", "Vemasse", "Venilale"],
    "aileu": ["Aileu Vila", "Laulara", "Lequidoe", "Remexio"],
}

PROGRAMS = [
    {"order": 1,
     "title": {"tet": "Edisaun daruak livru \"Buibere Hamriik Ukun Rasik An\"", "pt": "Segunda edição do livro \"Buibere Hamriik Ukun Rasik An\"", "id": "Edisi kedua buku \"Buibere Hamriik Ukun Rasik An\"", "en": "Second edition of \"Buibere Hamriik Ukun Rasik An\""},
     "description": {"tet": "Iha faze revizaun.", "pt": "Em fase de revisão.", "id": "Dalam tahap revisi.", "en": "Under revision."}},
    {"order": 2,
     "title": {"tet": "Publikasaun faze daruak kona-ba kontribuisaun Buibere", "pt": "Segunda fase da publicação sobre a contribuição das Buibere", "id": "Publikasi tahap kedua tentang kontribusi Buibere", "en": "Phase two of the publication on the Buibere's contribution"},
     "description": {
        "tet": "Kontribuisaun feto sira la'ós de'it ba luta libertasaun maibé ba Timor-Leste livre no independente. Livru dahuluk, ho apoiu Rede Feto, sei konta istória feto na'in-haat iha frente klandestina, armada no esterna.",
        "pt": "A contribuição das mulheres não só para a luta de libertação, mas também para um Timor-Leste livre e independente. O primeiro livro, com apoio da Rede Feto, contará a história de quatro mulheres nas frentes clandestina, armada e externa.",
        "id": "Kontribusi perempuan bukan hanya untuk perjuangan pembebasan, tetapi juga untuk Timor-Leste yang merdeka. Buku pertama, didukung Rede Feto, akan mengisahkan empat perempuan di front klandestin, bersenjata, dan luar negeri.",
        "en": "Women's contribution not only to the liberation struggle but to a free and independent Timor-Leste. The first book, supported by Rede Feto, will tell the stories of four women on the clandestine, armed and external fronts."}},
    {"order": 3,
     "title": {"tet": "Inskrisaun no re-inskrisaun membru OPMT", "pt": "Inscrição e reinscrição de membros", "id": "Pendaftaran dan pendaftaran ulang anggota", "en": "Member registration and renewal"},
     "description": {
        "tet": "Konsolidasaun OPMT iha teritóriu tomak no atribuisaun sertifikadu rekoñesimentu ba kuadru no membru sira.",
        "pt": "Consolidação da OPMT em todo o território e atribuição de certificados de reconhecimento a quadros e membros.",
        "id": "Konsolidasi OPMT di seluruh wilayah dan pemberian sertifikat penghargaan kepada kader dan anggota.",
        "en": "Strengthening OPMT across the country and awarding recognition certificates to cadres and members."}},
    {"order": 4,
     "title": {"tet": "Programa formasaun ba Buibere", "pt": "Programas de formação para as Buibere", "id": "Program pelatihan bagi Buibere", "en": "Training for Buibere"},
     "description": {"tet": "Kontinua programa formasaun ba Buibere sira.", "pt": "Continuação dos programas de formação.", "id": "Melanjutkan program pelatihan.", "en": "Ongoing training programmes."}},
    {"order": 5,
     "title": {"tet": "Apoiu ba projetu sósiu-ekonómiku feto nian", "pt": "Apoio a projectos socioeconómicos das mulheres", "id": "Dukungan proyek sosial-ekonomi perempuan", "en": "Support for women's livelihood projects"},
     "description": {"tet": "Liuliu iha área rurál sira.", "pt": "Sobretudo nas zonas rurais.", "id": "Terutama di daerah pedesaan.", "en": "Especially in rural areas."}},
]

ACTIVITIES = [
    {"category": "commemoration", "status": "done", "date": "2025-09-13", "location": "Sede CCF, Díli", "municipality": "dili",
     "title": {"tet": "Selebrasaun sinkuentenáriu OPMT", "pt": "Celebração do cinquentenário da OPMT", "id": "Perayaan 50 tahun OPMT", "en": "OPMT 50th anniversary celebration"},
     "summary": {"tet": "OPMT selebra tinan 50 no fó-sai vídeu-dokumentáriu kona-ba ninia istória.", "pt": "A OPMT celebra 50 anos e apresenta um vídeo-documentário sobre a sua história.", "id": "OPMT merayakan 50 tahun dan menayangkan video dokumenter tentang sejarahnya.", "en": "OPMT marks 50 years and premieres a documentary about its history."},
     "body": {
        "tet": "Iha 13 setembru 2025 OPMT selebra sinkuentenáriu iha sede CCF. Iha selebrasaun ne'e OPMT fó-sai vídeu-dokumentáriu ne'ebé uza testu perfil OPMT nian. RTM sei fó kópia vídeu ne'e.",
        "pt": "A 13 de Setembro de 2025 a OPMT celebrou o cinquentenário na sede do CCF, onde apresentou um vídeo-documentário baseado no texto do perfil da OPMT. A RTM disponibilizará cópia do vídeo.",
        "id": "Pada 13 September 2025 OPMT merayakan 50 tahun di gedung CCF dan menayangkan video dokumenter berdasarkan naskah profil OPMT. RTM akan menyediakan salinan videonya.",
        "en": "On 13 September 2025 OPMT celebrated its 50th anniversary at the CCF, premiering a documentary based on the OPMT profile text. RTM will provide a copy of the video."}},
    {"category": "publication", "status": "done", "location": "Díli", "municipality": "dili",
     "title": {"tet": "Espozisaun \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\"", "pt": "Exposição \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\"", "id": "Pameran \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\"", "en": "Exhibition \"Buibere Hamrik Tuba Rai Metin Ukun Rasik An\""},
     "summary": {"tet": "Painel espozisaun kona-ba kontribuisaun Buibere ba ukun rasik an, ho apoiu husi Gabinete de Apoio à Sociedade Civil.", "pt": "Painéis de exposição sobre a contribuição das Buibere para a independência, com apoio do Gabinete de Apoio à Sociedade Civil.", "id": "Panel pameran tentang kontribusi Buibere bagi kemerdekaan, didukung Gabinete de Apoio à Sociedade Civil.", "en": "Exhibition panels on the Buibere's contribution to independence, supported by the Civil Society Support Office."},
     "body": {
        "tet": "Espozisaun ne'e hatudu linha tempu OPMT no istória feto sira iha luta ba ukun rasik an. Painel sira mós akompaña livru \"Buibere Hamriik Ukun Rasik An\".",
        "pt": "A exposição apresenta a linha do tempo da OPMT e a história das mulheres na luta pela independência. Os painéis acompanham também o livro \"Buibere Hamriik Ukun Rasik An\".",
        "id": "Pameran ini menampilkan garis waktu OPMT dan kisah perempuan dalam perjuangan kemerdekaan. Panel-panelnya juga mendampingi buku \"Buibere Hamriik Ukun Rasik An\".",
        "en": "The exhibition presents OPMT's timeline and the story of women in the struggle for independence. The panels also accompany the book \"Buibere Hamriik Ukun Rasik An\"."}},
    {"category": "publication", "status": "done", "date": "2020-06-10", "location": "Díli", "municipality": "dili",
     "title": {"tet": "Lansamentu livru \"Buibere Hamriik Ukun Rasik An\"", "pt": "Lançamento do livro \"Buibere Hamriik Ukun Rasik An\"", "id": "Peluncuran buku \"Buibere Hamriik Ukun Rasik An\"", "en": "Book launch: \"Buibere Hamriik Ukun Rasik An\""},
     "summary": {"tet": "Prezidente Repúblika Francisco Guterres Lú Olo lansa livru OPMT kona-ba kontribuisaun feto ba luta libertasaun.", "pt": "O Presidente da República Francisco Guterres Lú Olo lança o livro da OPMT sobre a contribuição das mulheres para a luta de libertação.", "id": "Presiden Francisco Guterres Lú Olo meluncurkan buku OPMT tentang kontribusi perempuan dalam perjuangan pembebasan.", "en": "President Francisco Guterres Lú Olo launches OPMT's book on women's contribution to the liberation struggle."},
     "body": {
        "tet": "Livru ne'e hakerek husi Komisaun Peskiza no Hakerek ne'ebé OPMT harii no dirije.",
        "pt": "O livro foi escrito pela Comissão de Pesquisa e Escrita criada e dirigida pela OPMT.",
        "id": "Buku ini ditulis oleh Komisi Riset dan Penulisan yang dibentuk dan dipimpin OPMT.",
        "en": "The book was written by the Research and Writing Commission that OPMT set up and leads."}},
    {"category": "training", "status": "planned", "location": "Same", "municipality": "manufahi", "sample": True,
     "title": {"tet": "Formasaun lideransa ba Buibere (ezemplu)", "pt": "Formação de liderança para Buibere (exemplo)", "id": "Pelatihan kepemimpinan Buibere (contoh)", "en": "Leadership training for Buibere (sample)"},
     "summary": {"tet": "Atividade ezemplu. Troka ho atividade loos husi OPMT.", "pt": "Actividade de exemplo. Substituir por actividade real da OPMT.", "id": "Kegiatan contoh. Ganti dengan kegiatan nyata OPMT.", "en": "Sample activity. Replace with a real OPMT activity."},
     "body": {"tet": "Testu ezemplu.", "pt": "Texto de exemplo.", "id": "Teks contoh.", "en": "Sample text."}},
]

NEWS = [
    {"published_at": "2025-09-13",
     "title": {"tet": "OPMT selebra tinan 50 ho vídeu-dokumentáriu foun", "pt": "OPMT celebra 50 anos com novo vídeo-documentário", "id": "OPMT rayakan 50 tahun dengan video dokumenter baru", "en": "OPMT marks 50 years with a new documentary"},
     "excerpt": {"tet": "Selebrasaun iha sede CCF hanoin fila-fali dalan OPMT husi 1975 to'o ohin.", "pt": "A celebração na sede do CCF recordou o percurso da OPMT desde 1975.", "id": "Perayaan di gedung CCF mengenang perjalanan OPMT sejak 1975.", "en": "The celebration at the CCF looked back on OPMT's path since 1975."},
     "body": {
        "tet": "OPMT selebra sinkuentenáriu iha 13 setembru 2025 iha sede CCF. Vídeu-dokumentáriu foun konta istória organizasaun husi ninia fundasaun iha 28 agostu 1975, liuhusi rezisténsia, to'o restaurasaun independénsia no ohin loron.",
        "pt": "A OPMT celebrou o cinquentenário a 13 de Setembro de 2025 na sede do CCF. Um novo vídeo-documentário conta a história da organização desde a fundação, a 28 de Agosto de 1975, passando pela resistência, até à restauração da independência e aos dias de hoje.",
        "id": "OPMT merayakan 50 tahun pada 13 September 2025 di gedung CCF. Video dokumenter baru mengisahkan perjalanan organisasi sejak didirikan pada 28 Agustus 1975, melalui masa perlawanan, hingga pemulihan kemerdekaan dan hari ini.",
        "en": "OPMT celebrated its 50th anniversary on 13 September 2025 at the CCF. A new documentary tells the organisation's story from its founding on 28 August 1975, through the resistance, to the restoration of independence and today."}},
    {"published_at": "2025-08-22",
     "title": {"tet": "Omenajen ba Sekretária-Jeral Florentina Smith", "pt": "Homenagem à Secretária-Geral Florentina Smith", "id": "Penghormatan untuk Sekretaris Jenderal Florentina Smith", "en": "Tribute to Secretary-General Florentina Smith"},
     "excerpt": {"tet": "OPMT hatoo kondolénsia ba família no hanoin ninia kontribuisaun.", "pt": "A OPMT apresenta condolências à família e recorda o seu contributo.", "id": "OPMT menyampaikan belasungkawa kepada keluarga dan mengenang jasanya.", "en": "OPMT extends condolences to her family and remembers her service."},
     "body": {
        "tet": "Florentina Pereira da Conceição Martins Smith mate tanba moras iha 22 agostu 2025. Nia kaer knaar nu'udar Sekretária-Jeral interina husi 2021 no eleita iha IV Konferénsia Nasionál.",
        "pt": "Florentina Pereira da Conceição Martins Smith faleceu por doença a 22 de Agosto de 2025. Exerceu funções de Secretária-Geral interina desde 2021 e foi eleita na IV Conferência Nacional.",
        "id": "Florentina Pereira da Conceição Martins Smith wafat karena sakit pada 22 Agustus 2025. Ia menjabat Sekretaris Jenderal sementara sejak 2021 dan terpilih pada Konferensi Nasional IV.",
        "en": "Florentina Pereira da Conceição Martins Smith died after an illness on 22 August 2025. She served as interim Secretary-General from 2021 and was elected at the 4th National Conference."}},
]

DOCUMENTS = [
    {"category": "statute", "year": 2021, "language": "Português", "file": "estatutos-opmt.pdf",
     "title": {"tet": "Estatutu OPMT", "pt": "Estatuto da OPMT", "id": "Statuta OPMT", "en": "OPMT Statute"},
     "description": {
        "tet": "Matadalan OPMT, aprova iha 2016 no aprova fali iha Konferénsia Nasionál 2021.",
        "pt": "Documento orientador da OPMT, aprovado em 2016 e reaprovado na Conferência Nacional de 2021.",
        "id": "Pedoman OPMT, disahkan 2016 dan disahkan kembali pada Konferensi Nasional 2021.",
        "en": "OPMT's governing document, approved in 2016 and re-approved at the 2021 National Conference."}},
    {"category": "publication", "year": 2016, "language": "Tetun", "file": "espozisaun-buibere-hamrik.pdf",
     "title": {"tet": "Espozisaun \"Buibere Hamrik\" — kapa", "pt": "Exposição \"Buibere Hamrik\" — capa", "id": "Pameran \"Buibere Hamrik\" — sampul", "en": "\"Buibere Hamrik\" exhibition — cover"},
     "description": {
        "tet": "Kapa espozisaun OPMT ho apoiu husi Gabinete de Apoio à Sociedade Civil.",
        "pt": "Capa da exposição da OPMT, com apoio do Gabinete de Apoio à Sociedade Civil.",
        "id": "Sampul pameran OPMT, didukung Gabinete de Apoio à Sociedade Civil.",
        "en": "Cover of the OPMT exhibition, supported by the Civil Society Support Office."}},
]

SLIDES = [
    {"theme": "paper", "image": "slide-buibere-hamrik.jpg", "link": "/atividade",
     "title": {"tet": "Tinan 50 OPMT: 1975–2025", "pt": "50 anos da OPMT: 1975–2025", "id": "50 tahun OPMT: 1975–2025", "en": "50 years of OPMT: 1975–2025"},
     "text": {
        "tet": "Husi krexe dahuluk iha 1975 to'o selebrasaun sinkuentenáriu iha 13 setembru 2025.",
        "pt": "Da primeira creche em 1975 à celebração do cinquentenário a 13 de Setembro de 2025.",
        "id": "Dari tempat penitipan anak pertama pada 1975 hingga perayaan 50 tahun pada 13 September 2025.",
        "en": "From the first crèche in 1975 to the 50th anniversary celebration on 13 September 2025."},
     "button": {"tet": "Haree atividade", "pt": "Ver actividades", "id": "Lihat kegiatan", "en": "See activities"}},
    {"theme": "ink", "link": "/istoria",
     "title": {"tet": "Livru \"Buibere Hamriik Ukun Rasik An\"", "pt": "Livro \"Buibere Hamriik Ukun Rasik An\"", "id": "Buku \"Buibere Hamriik Ukun Rasik An\"", "en": "The book \"Buibere Hamriik Ukun Rasik An\""},
     "text": {
        "tet": "Kontribuisaun feto sira ba luta libertasaun nasionál. Edisaun daruak iha faze revizaun.",
        "pt": "A contribuição das mulheres para a luta de libertação nacional. A segunda edição está em revisão.",
        "id": "Kontribusi perempuan dalam perjuangan pembebasan nasional. Edisi kedua sedang direvisi.",
        "en": "Women's contribution to the national liberation struggle. A second edition is under revision."},
     "button": {"tet": "Lee istória", "pt": "Ler a história", "id": "Baca sejarah", "en": "Read the history"}},
    {"theme": "red", "link": "/sai-membru",
     "title": {"tet": "Sai membru OPMT", "pt": "Torne-se membro da OPMT", "id": "Jadi anggota OPMT", "en": "Become an OPMT member"},
     "text": {
        "tet": "Feto timor hotu ho tinan 16 ka liu bele rejista online. Estrutura OPMT iha ita-nia munisípiu sei kontaktu ita.",
        "pt": "Qualquer mulher timorense com 16 anos ou mais pode inscrever-se online. A estrutura da OPMT no seu município entrará em contacto.",
        "id": "Setiap perempuan Timor berusia 16 tahun ke atas bisa mendaftar online. Struktur OPMT di munisipiu Anda akan menghubungi Anda.",
        "en": "Any Timorese woman aged 16 or over can register online. The OPMT structure in your municipality will contact you."},
     "button": {"tet": "Rejista agora", "pt": "Inscrever-me", "id": "Daftar sekarang", "en": "Register now"}},
]
