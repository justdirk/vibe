#!/usr/bin/env python3
"""Generates /speaking/ and /{de,es,pt,it}/speaking/ from one template + per-locale strings.
Idempotent; the English strings are the source of truth for structure."""
import os
assert open("CNAME").read().strip() == "dirk.it"

NAV = {  # locale → nav labels + paths (mirrors the site nav)
 "en": dict(lang="en", pre="", courses="Courses", speaking="Speaking", about="About", cta="Book Dirk", enroll="Enroll", contact="Contact", privacy="Privacy", terms="Terms", tools="Tools", og="en_US"),
 "de": dict(lang="de", pre="/de", courses="Kurse", speaking="Keynotes", about="Über mich", cta="Dirk buchen", enroll="Jetzt starten", contact="Kontakt", privacy="Datenschutz", terms="AGB", tools="Tools", og="de_DE"),
 "es": dict(lang="es", pre="/es", courses="Cursos", speaking="Conferencias", about="Sobre mí", cta="Contratar a Dirk", enroll="Inscríbete", contact="Contacto", privacy="Privacidad", terms="Términos", tools="Herramientas", og="es_ES"),
 "pt": dict(lang="pt-BR", pre="/pt", courses="Cursos", speaking="Palestras", about="Sobre", cta="Contratar Dirk", enroll="Inscreva-se", contact="Contato", privacy="Privacidade", terms="Termos", tools="Ferramentas", og="pt_BR"),
 "it": dict(lang="it", pre="/it", courses="Corsi", speaking="Keynote", about="Chi sono", cta="Prenota Dirk", enroll="Iscriviti", contact="Contatti", privacy="Privacy", terms="Termini", tools="Strumenti", og="it_IT"),
}

S = {
 "en": dict(
  title="Speaking — Dirk Ahlborn",
  desc="Keynote speaker on innovation, crowd-powered companies and working in the age of AI. Founder of HyperloopTT, 80+ stages from Davos to Austin. Check availability.",
  eyebrow="Keynote speaker · Founder, HyperloopTT", h1="Put a builder on your stage.",
  lead="Innovation, crowd-powered companies, and what AI changes about how work gets done — from someone who turned an open whitepaper into an 800-person, 40-country company. In person or virtual, in English, German or Italian.",
  cta1="Check availability", cta2="Watch a keynote",
  p1="stages — WEF, SXSW, CES, DLD, Nikkei", p2="countries — keynotes on four continents", p3="Harvard Business School case studies on the model", p4="languages — English, German, Italian",
  watch="Watch", cap="KEYNOTE HIGHLIGHTS", watch_h="Not slides about the future. The story of building it.",
  watch_p="Every talk is grounded in what it actually took to build HyperloopTT — the deals, the failures, the 800 people who worked for equity — and ends with something the room can do on Monday.",
  talks="Talks", talks_h="Three keynotes, each with a takeaway you can act on.",
  t1="Building the Hyperloop", t1p="How an open whitepaper became a global company — the deals, the failures, and what moonshots teach about ordinary companies.",
  t1a="Why \"impossible\" is usually a resourcing problem, not a physics problem", t1b="How to sign partners and governments before you have a product", t1c="What nearly ended the company — and what saved it", t1f="Best for: corporate innovation, transport &amp; infrastructure, leadership offsites",
  t2="Crowd-Powered Companies", t2p="800 people in 40 countries working for equity instead of salaries — the model Harvard turned into two case studies, and how to apply it.",
  t2a="How to recruit world-class talent with no payroll", t2b="Governance that keeps a distributed crowd shipping", t2c="Where the model breaks, and the guardrails that stop it", t2f="Best for: founders, HR &amp; future-of-work, business schools",
  t3="Working in the Age of AI", t3p="What AI changes about how companies get built — and the practical playbook for leaders who refuse to be left behind.",
  t3a="The jobs inside your company AI already does better — and the ones it can't", t3b="A one-person company that runs like a fifty-person one", t3c="How to start Monday: the first three workflows to hand to an agent", t3f="Best for: executive audiences, industry associations, all-hands",
  stages="Selected stages",
  q1="\"He demonstrated to our 12,000 participants a new future of possibility. We recommend him as a speaker on stages around the world.\"", q1c="Open Innovation Forum",
  q2="\"Everybody was impressed by your very passionate speech. You have lit the audience's fire!\"", q2c="Global Business Bureau, Nikkei Inc.",
  formats="Formats", formats_h="Pick the shape that fits your programme.",
  f1="Keynote", f1p="20 to 60 minutes, with or without Q&amp;A. Tailored to your industry and audience.", f2="Fireside chat", f2p="A moderated conversation — great for founder audiences and investor events.", f3="Executive workshop", f3p="Half-day session on crowd-powered building or putting AI to work in your company.", f4="Virtual", f4p="Remote delivery for global town halls and online summits.",
  kit="Press kit",
  bio="Dirk Ahlborn is the founder of Hyperloop Transportation Technologies, the company that turned an open whitepaper into a global effort of 800+ contributors in 40 countries, with government partnerships on three continents and two Harvard Business School case studies on its crowd-powered model. A former Berlin banker who built and sold companies in Italy before incubating startups out of NASA Ames research, he now teaches founders and professionals how to build with crowds, capital and AI, and speaks on innovation and the future of work on stages worldwide.",
  copy="Copy bio", credit="Please credit as \"Dirk Ahlborn, founder of HyperloopTT\". Click a photo to open the full-size file.", h1img="Portrait · city", h2img="Portrait · capsule",
  booking="Booking", booking_h="Check availability.",
  booking_p="Tell us about the event and the budget you have in mind. Replies come from Dirk's office, usually within two working days, with availability and terms. Travel is arranged from wherever Dirk is that month, so one combined figure for fee and travel keeps things simple.",
  prefer="Prefer email?",
  l_event="Event name", ph_event="e.g. Future of Living Summit 2027", l_date="Date(s)", ph_date="18 Nov 2026, or 'spring 2027'", l_city="City &amp; country", ph_city="Riyadh, Saudi Arabia",
  l_format="Format", fo1="Keynote", fo2="Fireside chat", fo3="Executive workshop", fo4="Virtual", fo5="Not sure yet",
  l_aud="Audience size", au1="Under 100", au2="100–500", au3="500–2,000", au4="2,000+",
  l_budget="Budget for fee + travel", bu0="Select a range", bu1="Under $10,000", bu2="$10,000 – $25,000", bu3="$25,000 – $50,000", bu4="$50,000+", bu5="Travel only (no honorarium)", bu6="Prefer to discuss",
  l_name="Your name", l_email="Email", l_org="Organization", l_msg="Anything else", ph_msg="Theme of the event, who's in the room, what you'd like the audience to leave with.", send="Send inquiry →",
  alt="Dirk Ahlborn in front of a Hyperloop capsule", playlbl="Play keynote video"),
 "de": dict(
  title="Keynotes — Dirk Ahlborn",
  desc="Keynote-Speaker zu Innovation, Crowd-getriebenen Unternehmen und Arbeiten im KI-Zeitalter. Gründer von HyperloopTT, über 80 Bühnen von Davos bis Austin. Verfügbarkeit anfragen.",
  eyebrow="Keynote-Speaker · Gründer, HyperloopTT", h1="Ein Macher auf Ihrer Bühne.",
  lead="Innovation, Crowd-getriebene Unternehmen und was KI daran ändert, wie Arbeit erledigt wird — von jemandem, der aus einem offenen Whitepaper ein Unternehmen mit 800 Menschen in 40 Ländern gemacht hat. Vor Ort oder virtuell, auf Deutsch, Englisch oder Italienisch.",
  cta1="Verfügbarkeit anfragen", cta2="Keynote ansehen",
  p1="Bühnen — WEF, SXSW, CES, DLD, Nikkei", p2="Länder — Keynotes auf vier Kontinenten", p3="Harvard-Business-School-Fallstudien zum Modell", p4="Sprachen — Deutsch, Englisch, Italienisch",
  watch="Ansehen", cap="KEYNOTE-HIGHLIGHTS", watch_h="Keine Folien über die Zukunft. Die Geschichte, wie man sie baut.",
  watch_p="Jeder Vortrag beruht darauf, was es wirklich brauchte, um HyperloopTT aufzubauen — die Deals, die Rückschläge, die 800 Menschen, die für Anteile arbeiteten — und endet mit etwas, das der Saal am Montag umsetzen kann.",
  talks="Vorträge", talks_h="Drei Keynotes, jede mit einer Erkenntnis, die Sie umsetzen können.",
  t1="Building the Hyperloop", t1p="Wie aus einem offenen Whitepaper ein globales Unternehmen wurde — die Deals, die Rückschläge, und was Moonshots über gewöhnliche Firmen lehren.",
  t1a="Warum „unmöglich“ meist ein Ressourcenproblem ist, kein Physikproblem", t1b="Wie man Partner und Regierungen gewinnt, bevor es ein Produkt gibt", t1c="Was das Unternehmen fast beendet hätte — und was es gerettet hat", t1f="Ideal für: Corporate Innovation, Verkehr &amp; Infrastruktur, Führungskräfte-Offsites",
  t2="Crowd-Powered Companies", t2p="800 Menschen in 40 Ländern, die für Anteile statt Gehalt arbeiten — das Modell, aus dem Harvard zwei Fallstudien machte, und wie man es anwendet.",
  t2a="Wie man Weltklasse-Talente ohne Gehaltsliste gewinnt", t2b="Governance, mit der eine verteilte Crowd liefert", t2c="Wo das Modell bricht — und welche Leitplanken das verhindern", t2f="Ideal für: Gründer, HR &amp; Future of Work, Business Schools",
  t3="Arbeiten im KI-Zeitalter", t3p="Was KI daran ändert, wie Unternehmen entstehen — und das praktische Playbook für Führungskräfte, die nicht zurückbleiben wollen.",
  t3a="Die Jobs in Ihrem Unternehmen, die KI schon besser macht — und die, die sie nicht kann", t3b="Ein Ein-Personen-Unternehmen, das läuft wie eines mit fünfzig", t3c="So starten Sie am Montag: die ersten drei Workflows für einen Agenten", t3f="Ideal für: Executive-Publikum, Verbände, All-Hands",
  stages="Ausgewählte Bühnen",
  q1="„Er hat unseren 12.000 Teilnehmern eine neue Zukunft des Möglichen gezeigt. Wir empfehlen ihn als Speaker für Bühnen auf der ganzen Welt.“", q1c="Open Innovation Forum",
  q2="„Alle waren von Ihrer leidenschaftlichen Rede beeindruckt. Sie haben das Publikum entflammt!“", q2c="Global Business Bureau, Nikkei Inc.",
  formats="Formate", formats_h="Wählen Sie das Format, das zu Ihrem Programm passt.",
  f1="Keynote", f1p="20 bis 60 Minuten, mit oder ohne Q&amp;A. Auf Branche und Publikum zugeschnitten.", f2="Fireside Chat", f2p="Ein moderiertes Gespräch — ideal für Gründer- und Investoren-Events.", f3="Executive-Workshop", f3p="Halbtägige Session zu Crowd-getriebenem Aufbau oder KI im eigenen Unternehmen.", f4="Virtuell", f4p="Remote-Delivery für globale Townhalls und Online-Summits.",
  kit="Pressemappe",
  bio="Dirk Ahlborn ist Gründer von Hyperloop Transportation Technologies, dem Unternehmen, das ein offenes Whitepaper in eine globale Initiative mit über 800 Mitwirkenden in 40 Ländern verwandelte — mit Regierungspartnerschaften auf drei Kontinenten und zwei Fallstudien der Harvard Business School zum Crowd-Modell. Der frühere Berliner Banker baute und verkaufte Unternehmen in Italien, bevor er Startups aus der NASA-Ames-Forschung inkubierte. Heute lehrt er Gründer und Fachleute, mit Crowds, Kapital und KI aufzubauen, und spricht weltweit über Innovation und die Zukunft der Arbeit.",
  copy="Bio kopieren", credit="Bitte als „Dirk Ahlborn, Gründer von HyperloopTT“ nennen. Foto anklicken für die Datei in voller Größe.", h1img="Porträt · Stadt", h2img="Porträt · Kapsel",
  booking="Buchung", booking_h="Verfügbarkeit anfragen.",
  booking_p="Erzählen Sie uns vom Event und vom Budget, das Sie im Kopf haben. Die Antwort kommt aus Dirks Büro, meist innerhalb von zwei Werktagen, mit Verfügbarkeit und Konditionen. Die Anreise wird von dort organisiert, wo Dirk in dem Monat ist — eine Gesamtsumme für Honorar und Reise hält es einfach.",
  prefer="Lieber per E-Mail?",
  l_event="Name des Events", ph_event="z. B. Future of Living Summit 2027", l_date="Datum", ph_date="18. Nov. 2026 oder „Frühjahr 2027“", l_city="Stadt &amp; Land", ph_city="Riad, Saudi-Arabien",
  l_format="Format", fo1="Keynote", fo2="Fireside Chat", fo3="Executive-Workshop", fo4="Virtuell", fo5="Noch unklar",
  l_aud="Publikumsgröße", au1="Unter 100", au2="100–500", au3="500–2.000", au4="2.000+",
  l_budget="Budget für Honorar + Reise", bu0="Bereich wählen", bu1="Unter 10.000 $", bu2="10.000 – 25.000 $", bu3="25.000 – 50.000 $", bu4="50.000 $+", bu5="Nur Reisekosten (kein Honorar)", bu6="Lieber besprechen",
  l_name="Ihr Name", l_email="E-Mail", l_org="Organisation", l_msg="Sonstiges", ph_msg="Thema des Events, wer im Saal sitzt, was das Publikum mitnehmen soll.", send="Anfrage senden →",
  alt="Dirk Ahlborn vor einer Hyperloop-Kapsel", playlbl="Keynote-Video abspielen"),
 "es": dict(
  title="Conferencias — Dirk Ahlborn",
  desc="Conferenciante sobre innovación, empresas impulsadas por multitudes y el trabajo en la era de la IA. Fundador de HyperloopTT, más de 80 escenarios de Davos a Austin. Consulta disponibilidad.",
  eyebrow="Conferenciante · Fundador, HyperloopTT", h1="Sube a un constructor a tu escenario.",
  lead="Innovación, empresas impulsadas por multitudes y lo que la IA cambia en la forma de trabajar — de alguien que convirtió un whitepaper abierto en una empresa de 800 personas en 40 países. Presencial o virtual, en inglés, alemán o italiano.",
  cta1="Consultar disponibilidad", cta2="Ver una keynote",
  p1="escenarios — WEF, SXSW, CES, DLD, Nikkei", p2="países — keynotes en cuatro continentes", p3="casos de estudio de Harvard Business School sobre el modelo", p4="idiomas — inglés, alemán, italiano",
  watch="Ver", cap="MOMENTOS DE LA KEYNOTE", watch_h="No diapositivas sobre el futuro. La historia de construirlo.",
  watch_p="Cada charla se apoya en lo que realmente costó construir HyperloopTT — los acuerdos, los fracasos, las 800 personas que trabajaron por participaciones — y termina con algo que la sala puede hacer el lunes.",
  talks="Charlas", talks_h="Tres keynotes, cada una con una idea que puedes poner en práctica.",
  t1="Construir el Hyperloop", t1p="Cómo un whitepaper abierto se convirtió en una empresa global — los acuerdos, los fracasos y lo que los moonshots enseñan a las empresas corrientes.",
  t1a="Por qué «imposible» suele ser un problema de recursos, no de física", t1b="Cómo firmar con socios y gobiernos antes de tener un producto", t1c="Lo que casi acabó con la empresa — y lo que la salvó", t1f="Ideal para: innovación corporativa, transporte e infraestructura, offsites directivos",
  t2="Empresas impulsadas por multitudes", t2p="800 personas en 40 países trabajando por participaciones en lugar de salario — el modelo que Harvard convirtió en dos casos de estudio, y cómo aplicarlo.",
  t2a="Cómo reclutar talento de primer nivel sin nómina", t2b="La gobernanza que mantiene a una multitud distribuida entregando", t2c="Dónde se rompe el modelo, y las barreras que lo evitan", t2f="Ideal para: fundadores, RR. HH. y futuro del trabajo, escuelas de negocio",
  t3="Trabajar en la era de la IA", t3p="Lo que la IA cambia en cómo se construyen las empresas — y el playbook práctico para líderes que se niegan a quedarse atrás.",
  t3a="Los trabajos de tu empresa que la IA ya hace mejor — y los que no puede", t3b="Una empresa de una persona que funciona como una de cincuenta", t3c="Cómo empezar el lunes: los tres primeros flujos que delegar a un agente", t3f="Ideal para: públicos ejecutivos, asociaciones sectoriales, all-hands",
  stages="Escenarios seleccionados",
  q1="«Mostró a nuestros 12.000 participantes un nuevo futuro de posibilidades. Lo recomendamos como ponente en escenarios de todo el mundo.»", q1c="Open Innovation Forum",
  q2="«Todo el mundo quedó impresionado por su apasionado discurso. ¡Encendió al público!»", q2c="Global Business Bureau, Nikkei Inc.",
  formats="Formatos", formats_h="Elige el formato que encaja con tu programa.",
  f1="Keynote", f1p="De 20 a 60 minutos, con o sin preguntas. Adaptada a tu sector y tu público.", f2="Charla informal", f2p="Una conversación moderada — ideal para públicos de fundadores e inversores.", f3="Taller ejecutivo", f3p="Sesión de medio día sobre construir con multitudes o poner la IA a trabajar en tu empresa.", f4="Virtual", f4p="Intervención remota para town halls globales y cumbres online.",
  kit="Kit de prensa",
  bio="Dirk Ahlborn es el fundador de Hyperloop Transportation Technologies, la empresa que convirtió un whitepaper abierto en un esfuerzo global de más de 800 colaboradores en 40 países, con alianzas gubernamentales en tres continentes y dos casos de estudio de Harvard Business School sobre su modelo impulsado por multitudes. Exbanquero en Berlín, construyó y vendió empresas en Italia antes de incubar startups surgidas de la investigación de NASA Ames. Hoy enseña a fundadores y profesionales a construir con multitudes, capital e IA, y habla sobre innovación y el futuro del trabajo en escenarios de todo el mundo.",
  copy="Copiar bio", credit="Por favor, acredita como «Dirk Ahlborn, fundador de HyperloopTT». Haz clic en una foto para abrir el archivo a tamaño completo.", h1img="Retrato · ciudad", h2img="Retrato · cápsula",
  booking="Contratación", booking_h="Consulta disponibilidad.",
  booking_p="Cuéntanos sobre el evento y el presupuesto que tienes en mente. Las respuestas llegan desde la oficina de Dirk, normalmente en dos días laborables, con disponibilidad y condiciones. El viaje se organiza desde donde esté Dirk ese mes, así que una cifra combinada para honorarios y viaje lo hace más simple.",
  prefer="¿Prefieres email?",
  l_event="Nombre del evento", ph_event="p. ej. Future of Living Summit 2027", l_date="Fecha(s)", ph_date="18 nov 2026, o «primavera 2027»", l_city="Ciudad y país", ph_city="Riad, Arabia Saudí",
  l_format="Formato", fo1="Keynote", fo2="Charla informal", fo3="Taller ejecutivo", fo4="Virtual", fo5="Aún no lo sé",
  l_aud="Tamaño del público", au1="Menos de 100", au2="100–500", au3="500–2.000", au4="2.000+",
  l_budget="Presupuesto para honorarios + viaje", bu0="Selecciona un rango", bu1="Menos de 10.000 $", bu2="10.000 – 25.000 $", bu3="25.000 – 50.000 $", bu4="50.000 $+", bu5="Solo viaje (sin honorarios)", bu6="Prefiero hablarlo",
  l_name="Tu nombre", l_email="Email", l_org="Organización", l_msg="Algo más", ph_msg="Tema del evento, quién estará en la sala, qué te gustaría que el público se lleve.", send="Enviar solicitud →",
  alt="Dirk Ahlborn frente a una cápsula Hyperloop", playlbl="Reproducir vídeo de la keynote"),
 "pt": dict(
  title="Palestras — Dirk Ahlborn",
  desc="Palestrante sobre inovação, empresas movidas por multidões e trabalho na era da IA. Fundador da HyperloopTT, mais de 80 palcos de Davos a Austin. Consulte a disponibilidade.",
  eyebrow="Palestrante · Fundador, HyperloopTT", h1="Coloque um construtor no seu palco.",
  lead="Inovação, empresas movidas por multidões e o que a IA muda na forma de trabalhar — por alguém que transformou um whitepaper aberto em uma empresa de 800 pessoas em 40 países. Presencial ou virtual, em inglês, alemão ou italiano.",
  cta1="Consultar disponibilidade", cta2="Assistir a uma keynote",
  p1="palcos — WEF, SXSW, CES, DLD, Nikkei", p2="países — keynotes em quatro continentes", p3="estudos de caso da Harvard Business School sobre o modelo", p4="idiomas — inglês, alemão, italiano",
  watch="Assista", cap="MELHORES MOMENTOS", watch_h="Não são slides sobre o futuro. É a história de construí-lo.",
  watch_p="Cada palestra se baseia no que realmente foi preciso para construir a HyperloopTT — os acordos, os fracassos, as 800 pessoas que trabalharam por participação — e termina com algo que a plateia pode fazer na segunda-feira.",
  talks="Palestras", talks_h="Três keynotes, cada uma com uma lição que você pode aplicar.",
  t1="Construindo o Hyperloop", t1p="Como um whitepaper aberto virou uma empresa global — os acordos, os fracassos e o que os moonshots ensinam às empresas comuns.",
  t1a="Por que «impossível» costuma ser um problema de recursos, não de física", t1b="Como fechar com parceiros e governos antes de ter um produto", t1c="O que quase acabou com a empresa — e o que a salvou", t1f="Ideal para: inovação corporativa, transporte e infraestrutura, offsites de liderança",
  t2="Empresas movidas por multidões", t2p="800 pessoas em 40 países trabalhando por participação em vez de salário — o modelo que Harvard transformou em dois estudos de caso, e como aplicá-lo.",
  t2a="Como recrutar talentos de primeira sem folha de pagamento", t2b="A governança que mantém uma multidão distribuída entregando", t2c="Onde o modelo quebra, e as proteções que evitam isso", t2f="Ideal para: fundadores, RH e futuro do trabalho, escolas de negócios",
  t3="Trabalhando na era da IA", t3p="O que a IA muda na forma como as empresas são construídas — e o playbook prático para líderes que se recusam a ficar para trás.",
  t3a="Os trabalhos da sua empresa que a IA já faz melhor — e os que ela não consegue", t3b="Uma empresa de uma pessoa que funciona como uma de cinquenta", t3c="Como começar na segunda: os três primeiros fluxos para entregar a um agente", t3f="Ideal para: público executivo, associações setoriais, all-hands",
  stages="Palcos selecionados",
  q1="«Ele mostrou aos nossos 12.000 participantes um novo futuro de possibilidades. Recomendamos como palestrante em palcos do mundo todo.»", q1c="Open Innovation Forum",
  q2="«Todos ficaram impressionados com o seu discurso apaixonado. Você acendeu o fogo da plateia!»", q2c="Global Business Bureau, Nikkei Inc.",
  formats="Formatos", formats_h="Escolha o formato que cabe na sua programação.",
  f1="Keynote", f1p="De 20 a 60 minutos, com ou sem perguntas. Adaptada ao seu setor e ao seu público.", f2="Bate-papo", f2p="Uma conversa moderada — ótima para públicos de fundadores e investidores.", f3="Workshop executivo", f3p="Sessão de meio dia sobre construir com multidões ou colocar a IA para trabalhar na sua empresa.", f4="Virtual", f4p="Participação remota para town halls globais e eventos online.",
  kit="Kit de imprensa",
  bio="Dirk Ahlborn é o fundador da Hyperloop Transportation Technologies, a empresa que transformou um whitepaper aberto em um esforço global de mais de 800 colaboradores em 40 países, com parcerias governamentais em três continentes e dois estudos de caso da Harvard Business School sobre o seu modelo movido por multidões. Ex-banqueiro em Berlim, construiu e vendeu empresas na Itália antes de incubar startups nascidas da pesquisa da NASA Ames. Hoje ensina fundadores e profissionais a construir com multidões, capital e IA, e fala sobre inovação e o futuro do trabalho em palcos do mundo todo.",
  copy="Copiar bio", credit="Por favor, credite como «Dirk Ahlborn, fundador da HyperloopTT». Clique em uma foto para abrir o arquivo em tamanho real.", h1img="Retrato · cidade", h2img="Retrato · cápsula",
  booking="Contratação", booking_h="Consulte a disponibilidade.",
  booking_p="Conte sobre o evento e o orçamento que você tem em mente. As respostas vêm do escritório do Dirk, normalmente em até dois dias úteis, com disponibilidade e condições. A viagem é organizada de onde o Dirk estiver naquele mês, então um valor único para cachê e viagem simplifica tudo.",
  prefer="Prefere e-mail?",
  l_event="Nome do evento", ph_event="ex.: Future of Living Summit 2027", l_date="Data(s)", ph_date="18 nov 2026, ou «primavera de 2027»", l_city="Cidade e país", ph_city="Riade, Arábia Saudita",
  l_format="Formato", fo1="Keynote", fo2="Bate-papo", fo3="Workshop executivo", fo4="Virtual", fo5="Ainda não sei",
  l_aud="Tamanho da plateia", au1="Menos de 100", au2="100–500", au3="500–2.000", au4="2.000+",
  l_budget="Orçamento para cachê + viagem", bu0="Selecione uma faixa", bu1="Menos de US$ 10.000", bu2="US$ 10.000 – 25.000", bu3="US$ 25.000 – 50.000", bu4="US$ 50.000+", bu5="Só viagem (sem cachê)", bu6="Prefiro conversar",
  l_name="Seu nome", l_email="E-mail", l_org="Organização", l_msg="Algo mais", ph_msg="Tema do evento, quem estará na sala, o que você gostaria que a plateia levasse.", send="Enviar pedido →",
  alt="Dirk Ahlborn diante de uma cápsula Hyperloop", playlbl="Reproduzir vídeo da keynote"),
 "it": dict(
  title="Keynote — Dirk Ahlborn",
  desc="Keynote speaker su innovazione, aziende costruite con la crowd e lavoro nell'era dell'IA. Fondatore di HyperloopTT, oltre 80 palchi da Davos ad Austin. Verifica la disponibilità.",
  eyebrow="Keynote speaker · Fondatore, HyperloopTT", h1="Porta chi costruisce sul tuo palco.",
  lead="Innovazione, aziende costruite con la crowd e ciò che l'IA cambia nel modo di lavorare — da chi ha trasformato un whitepaper aperto in un'azienda di 800 persone in 40 paesi. Dal vivo o in virtuale, in italiano, inglese o tedesco.",
  cta1="Verifica la disponibilità", cta2="Guarda una keynote",
  p1="palchi — WEF, SXSW, CES, DLD, Nikkei", p2="paesi — keynote in quattro continenti", p3="casi di studio della Harvard Business School sul modello", p4="lingue — italiano, inglese, tedesco",
  watch="Guarda", cap="HIGHLIGHTS DELLA KEYNOTE", watch_h="Non slide sul futuro. La storia di come costruirlo.",
  watch_p="Ogni intervento parte da ciò che è servito davvero per costruire HyperloopTT — gli accordi, i fallimenti, le 800 persone che hanno lavorato per equity — e finisce con qualcosa che la sala può fare lunedì.",
  talks="Interventi", talks_h="Tre keynote, ognuna con un'idea da mettere in pratica.",
  t1="Costruire l'Hyperloop", t1p="Come un whitepaper aperto è diventato un'azienda globale — gli accordi, i fallimenti e cosa i moonshot insegnano alle aziende normali.",
  t1a="Perché «impossibile» è quasi sempre un problema di risorse, non di fisica", t1b="Come firmare con partner e governi prima di avere un prodotto", t1c="Cosa ha quasi chiuso l'azienda — e cosa l'ha salvata", t1f="Ideale per: innovazione aziendale, trasporti e infrastrutture, offsite di leadership",
  t2="Aziende costruite con la crowd", t2p="800 persone in 40 paesi che lavorano per equity invece che per stipendio — il modello che Harvard ha trasformato in due casi di studio, e come applicarlo.",
  t2a="Come reclutare talenti di livello mondiale senza busta paga", t2b="La governance che fa consegnare una crowd distribuita", t2c="Dove il modello si rompe, e i paletti che lo impediscono", t2f="Ideale per: founder, HR e futuro del lavoro, business school",
  t3="Lavorare nell'era dell'IA", t3p="Cosa cambia l'IA nel modo in cui nascono le aziende — e il playbook pratico per chi guida e non vuole restare indietro.",
  t3a="I lavori nella tua azienda che l'IA fa già meglio — e quelli che non sa fare", t3b="Un'azienda di una persona che gira come una da cinquanta", t3c="Da dove partire lunedì: i primi tre flussi da affidare a un agente", t3f="Ideale per: pubblico executive, associazioni di categoria, all-hands",
  stages="Palchi selezionati",
  q1="«Ha mostrato ai nostri 12.000 partecipanti un nuovo futuro possibile. Lo raccomandiamo come speaker sui palchi di tutto il mondo.»", q1c="Open Innovation Forum",
  q2="«Tutti sono rimasti colpiti dal suo discorso appassionato. Ha acceso il pubblico!»", q2c="Global Business Bureau, Nikkei Inc.",
  formats="Formati", formats_h="Scegli il formato adatto al tuo programma.",
  f1="Keynote", f1p="Da 20 a 60 minuti, con o senza Q&amp;A. Su misura per settore e pubblico.", f2="Fireside chat", f2p="Una conversazione moderata — ideale per platee di founder e investitori.", f3="Workshop executive", f3p="Mezza giornata su come costruire con la crowd o mettere l'IA al lavoro in azienda.", f4="Virtuale", f4p="Intervento da remoto per town hall globali e summit online.",
  kit="Press kit",
  bio="Dirk Ahlborn è il fondatore di Hyperloop Transportation Technologies, l'azienda che ha trasformato un whitepaper aperto in uno sforzo globale di oltre 800 collaboratori in 40 paesi, con partnership governative in tre continenti e due casi di studio della Harvard Business School sul suo modello costruito con la crowd. Ex banchiere a Berlino, ha fondato e venduto aziende in Italia prima di incubare startup nate dalla ricerca del NASA Ames. Oggi insegna a founder e professionisti a costruire con crowd, capitale e IA, e parla di innovazione e futuro del lavoro sui palchi di tutto il mondo.",
  copy="Copia bio", credit="Citare come «Dirk Ahlborn, fondatore di HyperloopTT». Clicca una foto per aprire il file a grandezza intera.", h1img="Ritratto · città", h2img="Ritratto · capsula",
  booking="Prenotazione", booking_h="Verifica la disponibilità.",
  booking_p="Raccontaci l'evento e il budget che hai in mente. Le risposte arrivano dall'ufficio di Dirk, di solito entro due giorni lavorativi, con disponibilità e condizioni. Il viaggio si organizza da dove si trova Dirk quel mese: una cifra unica per compenso e viaggio semplifica tutto.",
  prefer="Preferisci l'email?",
  l_event="Nome dell'evento", ph_event="es. Future of Living Summit 2027", l_date="Data/e", ph_date="18 nov 2026, oppure «primavera 2027»", l_city="Città e paese", ph_city="Riad, Arabia Saudita",
  l_format="Formato", fo1="Keynote", fo2="Fireside chat", fo3="Workshop executive", fo4="Virtuale", fo5="Non ancora deciso",
  l_aud="Dimensione del pubblico", au1="Meno di 100", au2="100–500", au3="500–2.000", au4="2.000+",
  l_budget="Budget per compenso + viaggio", bu0="Seleziona una fascia", bu1="Meno di 10.000 $", bu2="10.000 – 25.000 $", bu3="25.000 – 50.000 $", bu4="50.000 $+", bu5="Solo viaggio (nessun compenso)", bu6="Preferisco parlarne",
  l_name="Il tuo nome", l_email="Email", l_org="Organizzazione", l_msg="Altro", ph_msg="Tema dell'evento, chi c'è in sala, cosa vorresti che il pubblico porti a casa.", send="Invia richiesta →",
  alt="Dirk Ahlborn davanti a una capsula Hyperloop", playlbl="Riproduci il video della keynote"),
}

LANGBAR = {"en": "English", "de": "Deutsch", "es": "Español", "pt": "Português", "it": "Italiano"}
IMG_CITY = "https://d2ol7oe51mr4n9.cloudfront.net/user_3F0So49nurWetb0sObRtCUzVKwQ/8997d3e1-8994-4dfd-b3e1-b21fbc813d85.jpg"
IMG_CAP = "https://d2ol7oe51mr4n9.cloudfront.net/user_3F0So49nurWetb0sObRtCUzVKwQ/ef7391c5-5456-4a08-ba18-c7a8f665d76c.webp"

def langbar(loc):
    parts = []
    for k in ["en", "de", "es", "pt", "it"]:
        href = ("" if k == "en" else "/" + k) + "/speaking/"
        hl = "pt-BR" if k == "pt" else k
        style = 'font-size:13px;color:#E0B15C;font-weight:700;text-decoration:none' if k == loc else 'font-size:13px;color:#9B958A;text-decoration:none'
        parts.append(f'<a href="{href}" hreflang="{hl}" lang="{hl}" style="{style}"><span class="lb-full">{LANGBAR[k]}</span><span class="lb-ab">{k.upper()}</span></a>')
    return ('<!-- LANGBAR:start -->\n<style>.lb-ab{display:none}.lb-row a{display:inline-flex;align-items:center;min-height:34px}@media(max-width:560px){.lb-full{display:none}.lb-ab{display:inline}.lb-word{display:none}.lb-row{gap:14px !important;padding:5px 16px !important;justify-content:center !important}}</style>'
            '<div style="background:#0A0A09;border-bottom:1px solid rgba(255,255,255,.09);font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif"><div class="lb-row" style="max-width:1100px;margin:0 auto;padding:9px 22px;display:flex;justify-content:flex-end;align-items:center;gap:15px;flex-wrap:wrap"><span class="lb-word" style="font-size:11px;color:#8A8478;letter-spacing:.09em;text-transform:uppercase">Language</span>'
            + "".join(parts) + '</div></div>\n<!-- LANGBAR:end -->')

def footer(loc):
    n = NAV[loc]; p = n["pre"]
    NOOP = ' rel="noopener"'
    a = lambda h, l, ext=False: f'<a href="{h}" style="font-size:14px;color:#9B958A"{NOOP if ext else ""}>{l}</a>'
    return f'''  <footer class="site">
    <div class="sig" style="font-size:30px">Dirk Ahlborn</div>
    <div class="footlinks">
      <div class="footrow">{a(p+"/courses/", n["courses"])}
      {a(p+"/speaking/", n["speaking"])}
      {a(p+"/about/", n["about"])}
      {a(p+"/culinaris/", "Culinaris")}
      {a("/contact/", n["contact"])}
      {a("/privacy/", n["privacy"])}
      {a("/terms/", n["terms"])}</div>
      <div class="footrow"><span class="footlbl">{n["tools"]}</span>{a("/chat/", "dirk.it AI")}
      {a("https://starterfuel.com", "StarterFuel", True)}
      {a("https://dna.dirk.it", "Venture DNA", True)}
      {a("https://remixer.dirk.it", "Remixer", True)}
      {a("https://pressduo.com", "PressDuo", True)}
      {a("https://condivida.com", "Condivida", True)}</div>
    </div>
    <div style="font-size:13px;color:#8A8478">© 2026 Dirk Ahlborn · <a href="{p or "/"}{"/" if p else ""}" style="color:#E0B15C">dirk.it</a></div>
  </footer>'''

def page(loc):
    s = S[loc]; n = NAV[loc]; p = n["pre"]; url = f"https://dirk.it{p}/speaking/"
    home = (p + "/") if p else "/"
    return f'''<!DOCTYPE html>
<html lang="{n["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s["title"]}</title>
<meta name="description" content="{s["desc"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Mrs+Saint+Delafield&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/site.css">
<link rel="stylesheet" href="/speaking.css">
<!-- SEO:start -->
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="https://dirk.it/speaking/">
<link rel="alternate" hreflang="de" href="https://dirk.it/de/speaking/">
<link rel="alternate" hreflang="es" href="https://dirk.it/es/speaking/">
<link rel="alternate" hreflang="pt-BR" href="https://dirk.it/pt/speaking/">
<link rel="alternate" hreflang="it" href="https://dirk.it/it/speaking/">
<link rel="alternate" hreflang="x-default" href="https://dirk.it/speaking/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dirk Ahlborn">
<meta property="og:title" content="{s["title"]}">
<meta property="og:description" content="{s["desc"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{IMG_CAP}">
<meta property="og:locale" content="{n["og"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{s["title"]}">
<meta name="twitter:description" content="{s["desc"]}">
<meta name="twitter:image" content="{IMG_CAP}">
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"Person","@id":"https://dirk.it/#dirk","name":"Dirk Ahlborn","url":"https://dirk.it/","jobTitle":"Founder & CEO, HyperloopTT","description":"Entrepreneur, educator and keynote speaker on innovation, crowd-powered companies and working in the age of AI. 80+ stages worldwide.","knowsLanguage":["en","de","it"],"image":"{IMG_CAP}"}},{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Dirk Ahlborn","item":"https://dirk.it{home}"}},{{"@type":"ListItem","position":2,"name":"{n["speaking"]}","item":"{url}"}}]}}]}}</script>
<!-- SEO:end -->
</head>
<body>
{langbar(loc)}

<div style="min-height:100vh;background:#0A0A09;color:#F2EFE9">
  <nav class="top">
    <a href="{home}" class="sig" style="font-size:34px">Dirk Ahlborn</a>
    <div class="links">
      <a href="{p}/courses/">{n["courses"]}</a>
      <a href="{p}/speaking/" class="on">{n["speaking"]}</a>
      <a href="{p}/about/">{n["about"]}</a>
      <a href="/chat/" class="ai">dirk.it AI</a>
      <a href="https://starterfuel.com" class="sf navSecondary" rel="noopener">StarterFuel</a>
      <a href="#inquire" class="cta">{n["cta"]}</a>
    </div>
  </nav>

  <section class="shero">
    <div class="img" role="img" aria-label="{s["alt"]}"></div>
    <div class="shade"></div><div class="shade2"></div>
    <div class="copy">
      <div class="eyebrow">{s["eyebrow"]}</div>
      <h1>{s["h1"]}</h1>
      <p>{s["lead"]}</p>
      <div class="ctas">
        <a href="#inquire" class="btnGold">{s["cta1"]}</a>
        <a href="#watch" class="btnGhost">{s["cta2"]}</a>
      </div>
    </div>
  </section>

  <section class="proof">
    <div><b>80+</b><span>{s["p1"]}</span></div>
    <div><b>40+</b><span>{s["p2"]}</span></div>
    <div><b>2</b><span>{s["p3"]}</span></div>
    <div><b>3</b><span>{s["p4"]}</span></div>
  </section>

  <section class="wrap" id="watch">
    <div class="watch">
      <div class="facade" id="facade" role="button" tabindex="0" aria-label="{s["playlbl"]}">
        <div class="play"><svg width="30" height="30" viewBox="0 0 24 24" fill="#0A0A09"><path d="M8 5v14l11-7z"/></svg></div>
        <div class="cap">{s["cap"]}</div>
      </div>
      <div class="side">
        <div class="eyebrow">{s["watch"]}</div>
        <h2 class="h2">{s["watch_h"]}</h2>
        <p>{s["watch_p"]}</p>
      </div>
    </div>
  </section>

  <section class="wrap tight">
    <div class="eyebrow">{s["talks"]}</div>
    <h2 class="h2 mt">{s["talks_h"]}</h2>
    <div class="talks">
      <div class="talk"><h3>{s["t1"]}</h3><p class="promise">{s["t1p"]}</p><ul><li>{s["t1a"]}</li><li>{s["t1b"]}</li><li>{s["t1c"]}</li></ul><div class="for">{s["t1f"]}</div></div>
      <div class="talk"><h3>{s["t2"]}</h3><p class="promise">{s["t2p"]}</p><ul><li>{s["t2a"]}</li><li>{s["t2b"]}</li><li>{s["t2c"]}</li></ul><div class="for">{s["t2f"]}</div></div>
      <div class="talk"><h3>{s["t3"]}</h3><p class="promise">{s["t3p"]}</p><ul><li>{s["t3a"]}</li><li>{s["t3b"]}</li><li>{s["t3c"]}</li></ul><div class="for">{s["t3f"]}</div></div>
    </div>
  </section>

  <section class="wrap tight">
    <div class="eyebrow">{s["stages"]}</div>
    <div class="stages">
      <span>World Economic Forum</span><span>SXSW</span><span>CES</span><span>DLD</span><span>Pioneers</span><span>Nikkei Forum</span><span>Open Innovation Forum</span>
    </div>
    <div class="quotes">
      <blockquote><p>{s["q1"]}</p><cite>{s["q1c"]}</cite></blockquote>
      <blockquote><p>{s["q2"]}</p><cite>{s["q2c"]}</cite></blockquote>
    </div>
  </section>

  <section class="wrap tight">
    <div class="eyebrow">{s["formats"]}</div>
    <h2 class="h2 mt">{s["formats_h"]}</h2>
    <div class="formats">
      <div><b>{s["f1"]}</b><span>{s["f1p"]}</span></div>
      <div><b>{s["f2"]}</b><span>{s["f2p"]}</span></div>
      <div><b>{s["f3"]}</b><span>{s["f3p"]}</span></div>
      <div><b>{s["f4"]}</b><span>{s["f4p"]}</span></div>
    </div>
  </section>

  <section class="wrap tight" id="presskit">
    <div class="eyebrow">{s["kit"]}</div>
    <div class="kit">
      <div class="bioBox">
        <p class="bio" id="bio">{s["bio"]}</p>
        <button class="copybtn" type="button" data-copy="bio">{s["copy"]}</button>
        <p class="note">{s["credit"]}</p>
      </div>
      <div class="heads">
        <a href="{IMG_CITY}" target="_blank" rel="noopener" style="background-image:url('{IMG_CITY}');background-position:20% 15%"><span>{s["h1img"]}</span></a>
        <a href="{IMG_CAP}" target="_blank" rel="noopener" style="background-image:url('{IMG_CAP}')"><span>{s["h2img"]}</span></a>
      </div>
    </div>
  </section>

  <section class="wrap" id="inquire" style="border-top:1px solid rgba(242,239,233,.1)">
    <div class="inq">
      <div class="side">
        <div class="eyebrow">{s["booking"]}</div>
        <h2 class="h2">{s["booking_h"]}</h2>
        <p>{s["booking_p"]}</p>
        <p class="note">{s["prefer"]} <a href="mailto:mail@dirk.it?subject=Speaking%20inquiry">mail@dirk.it</a></p>
      </div>
      <form class="book" id="book" novalidate>
        <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <label class="full">{s["l_event"]}<input name="event_name" required placeholder="{s["ph_event"]}"></label>
        <label>{s["l_date"]}<input name="event_date" required placeholder="{s["ph_date"]}"></label>
        <label>{s["l_city"]}<input name="event_city" required placeholder="{s["ph_city"]}"></label>
        <label>{s["l_format"]}<select name="event_format"><option>{s["fo1"]}</option><option>{s["fo2"]}</option><option>{s["fo3"]}</option><option>{s["fo4"]}</option><option>{s["fo5"]}</option></select></label>
        <label>{s["l_aud"]}<select name="audience_size"><option>{s["au1"]}</option><option>{s["au2"]}</option><option>{s["au3"]}</option><option>{s["au4"]}</option></select></label>
        <label class="full">{s["l_budget"]}<select name="budget_range"><option value="">{s["bu0"]}</option><option>{s["bu1"]}</option><option>{s["bu2"]}</option><option>{s["bu3"]}</option><option>{s["bu4"]}</option><option>{s["bu5"]}</option><option>{s["bu6"]}</option></select></label>
        <label>{s["l_name"]}<input name="name" required autocomplete="name"></label>
        <label>{s["l_email"]}<input name="email" type="email" required autocomplete="email"></label>
        <label class="full">{s["l_org"]}<input name="company" autocomplete="organization"></label>
        <label class="full">{s["l_msg"]}<textarea name="message" required placeholder="{s["ph_msg"]}"></textarea></label>
        <div id="fmsg" class="msg" hidden></div>
        <button class="btnGold" type="submit" id="fbtn">{s["send"]}</button>
      </form>
    </div>
  </section>

{footer(loc)}
</div>
<script src="/speaking.js" defer></script>
<script defer src="/a.js"></script>
</body>
</html>
'''

changed = 0
for loc in ["en", "de", "es", "pt", "it"]:
    path = ("speaking" if loc == "en" else f"{loc}/speaking") + "/index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html = page(loc)
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != html:
        open(path, "w", encoding="utf-8").write(html); changed += 1
print(f"{changed} files changed")
