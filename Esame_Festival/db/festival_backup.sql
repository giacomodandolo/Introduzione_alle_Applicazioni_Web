BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "ARTIST" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL UNIQUE,
	"image"	VARCHAR(255) NOT NULL,
	"short_description"	VARCHAR(100) NOT NULL,
	"description"	VARCHAR(512) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "PERFORMANCE" (
	"id"	INTEGER NOT NULL,
	"start_date"	DATETIME NOT NULL,
	"end_date"	DATETIME NOT NULL,
	"music_genre"	VARCHAR(100) NOT NULL,
	"description"	VARCHAR(512) NOT NULL,
	"image"	VARCHAR(255),
	"published"	INTEGER NOT NULL,
	"artist_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"stage_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("artist_id") REFERENCES "ARTIST"("id"),
	FOREIGN KEY("stage_id") REFERENCES "STAGE"("id"),
	FOREIGN KEY("user_id") REFERENCES "USER"("id")
);
CREATE TABLE IF NOT EXISTS "STAGE" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"description"	VARCHAR(512) NOT NULL,
	"image"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "TICKET" (
	"id"	INTEGER NOT NULL,
	"start_date"	DATETIME NOT NULL,
	"type"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "USER" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"surname"	VARCHAR(100) NOT NULL,
	"email"	VARCHAR(128) NOT NULL UNIQUE,
	"password"	VARCHAR(255) NOT NULL,
	"type"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "ARTIST" VALUES (1,'Mick Gordon','mick gordon_1749499975.webp','Compositore australiano conosciuto per Doom Eternal.','Mick Gordon ha composto per diversi sparatutto in prima persona, tra cui Atomic Heart, LawBreakers, Wolfenstein: The New Order, Wolfenstein: The Old Blood, Prey, il morbido reboot di Doom e il suo sequel Doom Eternal, Wolfenstein II: The New Colossus e le');
INSERT INTO "ARTIST" VALUES (2,'Capcom Sound Team','capcom sound team_1749500121.webp','Team delle musiche di Capcom.','Capcom Sound Team è lo staff sonoro di Capcom, formato da molteplici compositori responsabili della musica e degli effetti sonori dei giochi di Capcom, nonché dall''editore di album musicali per Capcom, comprese le pubblicazioni fisiche e digitali di album');
INSERT INTO "ARTIST" VALUES (3,'Gerard Marino','gerard marino_1749500280.webp','Compositore di musica per film e videogiochi.','Gerard Kendrick Marino (nato 1 aprile 1968) è un compositore di film e videogiochi, che ha contribuito, in particolare, molto ai giochi della serie greca di God of War.');
INSERT INTO "ARTIST" VALUES (4,'Jamie Christopherson','jamie christopherson_1749500443.webp','Musicista americano che ha contribuito in vari film e videogiochi.','Jamie Christopherson è un musicista americano che ha contribuito a numerosi film e videogiochi popolari, tra cui il film The Crow: Wicked Prayer e i giochi Onimusha: Dawn of Dreams e Metal Gear Rising: Revengeance.');
INSERT INTO "ARTIST" VALUES (5,'Naoki','naoki_1749500628.webp','Cantante giapponese, conosciuto per Guilty Gear.','Naoki Hashimoto, conosciuto anche come NAOKI, è un cantante giapponese che ha fornito la voce per una serie di canzoni della serie Guilty Gear dai tempi di Guilty Gear da Guilty Gear.');
INSERT INTO "ARTIST" VALUES (6,'Nobuo Uematsu','nobuo uematsu_1749500765.webp','Compositore giapponese conosciuto per Final Fantasy.','Nobuo Uematsu, nato il 21 marzo 1959, è un compositore e tastierista giapponese noto per i suoi contributi alla serie di videogiochi Final Fantasy di Square Enix. Musicista autodidatta, ha iniziato a suonare il pianoforte all''età di dodici anni, con il cantautore inglese Elton John come una delle sue più grandi influenze nel perseguire una carriera musicale.');
INSERT INTO "ARTIST" VALUES (7,'Martin O''Donnell','martin o''donnell_1749500897.webp','Compositore statunitense, noto per Halo.','Martin O''Donnell (nato il 1o maggio 1955) è un compositore, regista audio e sound designer americano noto per il suo lavoro sugli sviluppatori di videogiochi Bungie, come la serie Myth, Oni, la serie Halo e Destiny. O''Donnell ha collaborato con Michael Salvatori per tutte le partiture; ha anche diretto il talento vocale e il sound design per la trilogia di Halo.');
INSERT INTO "ARTIST" VALUES (8,'Darren Korb','darren korb_1749501015.webp','Compositore americano, conosciuto per Hades.','Darren Korb (Chicago, 5 novembre 1983) è un cantautore, compositore e doppiatore statunitense. Korb è meglio conosciuto per aver scritto la musica presente in Bastion, Transistor, Pyre, Hades e Hades II, che sono stati tutti sviluppati dallo sviluppatore indie Supergiant Games. Korb ha anche recitato a voce in questi ultimi due giochi, fornendo la voce al protagonista Zagreus in Hades.');
INSERT INTO "ARTIST" VALUES (9,'Nine Inch Nails','nine inch nails_1749501159.webp','Band rock.','Nine Inch Nails, comunemente abbreviato in NIN (stilizzato come NIИ), è un gruppo rock industriale statunitense formatosi a Cleveland, Ohio nel 1988. I suoi membri sono il cantautore, polistrumentista e produttore Trent Reznor e il suo frequente collaboratore, Atticus Ross.');
INSERT INTO "ARTIST" VALUES (10,'zYnthetic','zynthetic_1749501343.webp','Musicista e sound designer, conosciuto per Killing Floor.','Musicista e sound designer, conosciuto per Killing Floor.');
INSERT INTO "ARTIST" VALUES (11,'Christopher Larkin','christopher larkin_1749501490.webp','Compositore australiano, noto per Hollow Knight.','Christopher James Larkin è un compositore australiano per videogiochi, film e televisione, meglio conosciuto per il suo lavoro su Hollow Knight (2017) e il suo sequel Hollow Knight: Silksong (2025). Alcune delle sue altre opere includono Pac-Man 256, Outfolded, TOHU e Hacknet.');
INSERT INTO "ARTIST" VALUES (12,'Hikaru Utada','hikaru utada_1749501622.webp','Cantante giapponese e americana, nota per Kingdom Hearts.','Hikaru Utada, nata il 19 gennaio 1983, conosciuta anche come Utada, è una cantante, cantautrice e produttrice giapponese e americana. È considerata una delle artiste musicali più influenti e più vendute in Giappone. È meglio conosciuta dal pubblico internazionale per aver scritto e prodotto quattro contributi a tema alla serie di videogiochi collaborativi di Square Enix e Disney Kingdom Hearts: "Simple and Clean", "Sanctuary", "Don''t Think Twice" e "Face My Fears".');
INSERT INTO "ARTIST" VALUES (13,'Motoi Sakuraba','motoi sakuraba_1749501721.webp','Compositore giapponese, noto per Dark Souls.','Motoi Sakuraba, nata il 5 agosto 1965, è una compositrice e tastierista giapponese. È noto per i suoi numerosi contributi nei videogiochi, tra cui i Tales, Star Ocean, Mario Golf, Mario Tennis, Golden Sun e Dark Souls, così come diverse altre serie anime, drammi televisivi e album progressive rock.');
INSERT INTO "ARTIST" VALUES (14,'Masters of Sound','masters of sound_1749501901.webp','Band che crea cover di musiche per videogiochi.','Band che crea cover di musiche per videogiochi.');
INSERT INTO "ARTIST" VALUES (15,'Jeremy Soule','jeremy soule_1749502055.webp','Compositore americano, conosciuto per The Elder Scrolls.','Jeremy Soule (in tedesco SOHL; nato il 19 dicembre 1975) è un compositore americano di colonne sonore per film, televisione e videogiochi. Ha composto colonne sonore per oltre 60 giochi e oltre una dozzina di altri lavori durante la sua carriera, tra cui The Elder Scrolls, Guild Wars, Total Annihilation e la serie di Harry Potter.');
INSERT INTO "PERFORMANCE" VALUES (1,'2025-07-18T13:00','2025-07-18T14:00','Metal','Entriamo nel fantastico mondo di Mick Gordon!','mick gordon_performance_1749499975.webp',1,1,1,2);
INSERT INTO "PERFORMANCE" VALUES (2,'2025-07-18T15:00','2025-07-18T16:00','Metal','Entriamo nel fantastico mondo del Capcom Sound Team!','capcom sound team_performance_1749500121.webp',1,2,1,2);
INSERT INTO "PERFORMANCE" VALUES (3,'2025-07-18T11:00','2025-07-18T11:40','Metal','Entriamo nel fantastico mondo di Gerard Marino!','gerard marino_performance_1749500280.webp',1,3,1,2);
INSERT INTO "PERFORMANCE" VALUES (4,'2025-07-18T10:00','2025-07-18T10:40','Metal','Entriamo nel mondo fantastico di Jamie Christopherson!','jamie christopherson_performance_1749500443.webp',1,4,1,2);
INSERT INTO "PERFORMANCE" VALUES (5,'2025-07-18T14:00','2025-07-18T14:50','Metal','Entriamo nel fantastico mondo di NAOKI!','naoki_performance_1749500628.webp',0,5,1,2);
INSERT INTO "PERFORMANCE" VALUES (6,'2025-07-19T15:00','2025-07-19T16:00','Rock','Entriamo nel fantastico mondo di Nobuo Uematsu!','nobuo uematsu_performance_1749500765.webp',1,6,1,3);
INSERT INTO "PERFORMANCE" VALUES (7,'2025-07-19T13:00','2025-07-19T13:50','Rock','Entriamo nel fantastico mondo di Martin O''Donnell!','martin o''donnell_performance_1749500897.webp',1,7,1,3);
INSERT INTO "PERFORMANCE" VALUES (8,'2025-07-19T14:00','2025-07-19T14:40','Rock','Entriamo nel fantastico mondo di Darren Korb!','darren korb_performance_1749501015.webp',1,8,1,3);
INSERT INTO "PERFORMANCE" VALUES (9,'2025-07-19T16:00','2025-07-19T17:00','Rock','Entriamo nel fantastico mondo dei Nine Inch Kills!','nine inch nails_performance_1749501159.webp',1,9,1,3);
INSERT INTO "PERFORMANCE" VALUES (10,'2025-07-19T17:00','2025-07-19T17:40','Rock','Entriamo nel fantastico mondo di zYnthetic!','zynthetic_performance_1749501343.webp',0,10,1,3);
INSERT INTO "PERFORMANCE" VALUES (11,'2025-07-20T14:00','2025-07-20T14:45','Musica classica','Entriamo nel fantastico mondo di Christopher Larkin!','christopher larkin_performance_1749501490.webp',1,11,1,1);
INSERT INTO "PERFORMANCE" VALUES (12,'2025-07-20T15:00','2025-07-20T15:45','Musica classica','Entriamo nel fantastico mondo di Hikaru Utada!','hikaru utada_performance_1749501622.webp',1,12,1,1);
INSERT INTO "PERFORMANCE" VALUES (13,'2025-07-20T17:00','2025-07-20T17:50','Musica classica','Entriamo nel fantastico mondo di Motoi Sakuraba!','motoi sakuraba_performance_1749501721.webp',1,13,1,1);
INSERT INTO "PERFORMANCE" VALUES (14,'2025-07-20T16:00','2025-07-20T16:50','Musica classica','Entriamo nel fantastico mondo dei Masters of Sound!','masters of sound_performance_1749501901.webp',1,14,1,1);
INSERT INTO "PERFORMANCE" VALUES (15,'2025-07-20T18:00','2025-07-20T19:10','Musica classica','Entriamo nel fantastico mondo di Jeremy Soule!','jeremy soule_performance_1749502055.webp',0,15,2,1);
INSERT INTO "STAGE" VALUES (1,'The Mantis Village','Palco nelle profondità di Hallownest, dove si sopravvive dimostrando la propria forza.','mantis_village_stage.webp');
INSERT INTO "STAGE" VALUES (2,'Jekkad','A partire da dove nascono i demoni, nasce anche la musica metal migliore nel mondo del gaming.','jekkad_stage.webp');
INSERT INTO "STAGE" VALUES (3,'Midgar','La leggendaria città diventa il palco della musica rock più iconica del mondo del gaming.','midgar_stage.webp');
INSERT INTO "TICKET" VALUES (1,'2025-07-19T00:00',0,3);
INSERT INTO "TICKET" VALUES (2,'2025-07-19T00:00',1,4);
INSERT INTO "TICKET" VALUES (3,'2025-07-18T00:00',2,5);
INSERT INTO "USER" VALUES (1,'Primo','Collaboratore','primo.collaboratore@mail.com','scrypt:32768:8:1$3tPQEV2pDzJQ9ovL$3b29983c91c2713f59546bd4695f3495c27e13482860df6ad2faef01a581633a2d8f54746a9965549d93fd40544fd6edca39dfd29fdd10b6fc1191e53a2c937d',2);
INSERT INTO "USER" VALUES (2,'Secondo','Collaboratore','secondo.collaboratore@mail.com','scrypt:32768:8:1$KEORHD9YZGZ9eqPW$2e3e3e665aa7cc403ca194eb56fbb634df5d6ff586e4a2899575dc7a66c72f228060327c7d3f9024f1942070ad82a7683abc74efda2b9c71884d62fe8f7b5768',2);
INSERT INTO "USER" VALUES (3,'Primo','Partecipante','primo.partecipante@mail.com','scrypt:32768:8:1$Ifp46RLmdag0EyeW$067885a951c8222c83a9823eb83acd3970c1f41ac62ca4a8cab8edc5e7c6313ad54730eada5acc9266359d3d5b49e75ec971d1f4737dffd5812b023f746735ec',1);
INSERT INTO "USER" VALUES (4,'Secondo','Partecipante','secondo.partecipante@mail.com','scrypt:32768:8:1$Q06fLK6exfpdCNYr$26550bc8f0aa6d062ca7c07faca2721398a15d4156b680a90e4620d9385b6b48028398e738c36730ec6c8f8245b5bb430996368d6548b8d469c34b96042be770',1);
INSERT INTO "USER" VALUES (5,'Terzo','Partecipante','terzo.partecipante@mail.com','scrypt:32768:8:1$WccN0o9tXtFAhyWu$07df1653354491ae37ff2cfcdaded897cc04a43e84ad224a3d56b61c55d579f5134494065a416b4c0ccf1571cb2be682c8a02b36b7a39b7f0d95e6a773e7440d',1);
COMMIT;
