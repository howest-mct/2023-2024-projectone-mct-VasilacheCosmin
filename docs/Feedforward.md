# Projectgegevens

**VOORNAAM NAAM:** Andrei Vasilache

**Sparringpartner:** Warre Snaet

**Projectsamenvatting in max 10 woorden:** GPS-tracker voor elektrische step

**Projecttitel:** I-track

# Tips voor feedbackgesprekken

## Voorbereiding

> Bepaal voor jezelf waar je graag feedback op wil. Schrijf op voorhand een aantal punten op waar je zeker feedback over wil krijgen. Op die manier zal het feedbackgesprek gerichter verlopen en zullen vragen, die je zeker beantwoord wil hebben, aan bod komen.

## Tijdens het gesprek:

> **Luister actief:** Schiet niet onmiddellijk in de verdediging maar probeer goed te luisteren. Laat verbaal en non-verbaal ook zien dat je aandacht hebt voor de feedback door een open houding (oogcontact, rechte houding), door het maken van aantekeningen, knikken...

> **Maak notities:** Schrijf de feedback op zo heb je ze nog nadien. Noteer de kernwoorden en zoek naar een snelle noteer methode voor jezelf. Als je goed noteert,kan je op het einde van het gesprek je belangrijkste feedback punten kort overlopen.

> **Vat samen:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.

> **Sta open voor de feedback:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.`

> **Denk erover na:** Denk na over wat je met de feedback gaat doen en koppel terug. Vind je de opmerkingen terecht of onterecht? Herken je je in de feedback? Op welke manier ga je dit aanpakken?

## NA HET GESPREK

> Herlees je notities en maak actiepunten. Maak keuzes uit alle feedback die je kreeg: Waar kan je mee aan de slag en wat laat je even rusten. Wat waren de prioriteiten? Neem de opdrachtfiche er nog eens bij om je focuspunten te bepalen.Noteer je actiepunten op de feedbackfiche.

# Feedforward gesprekken

## Gesprek 1 (Datum: 23/05/2024)

Lector: Pieter-Jan Vidts

Vragen voor dit gesprek: 

- vraag 1: Wat kan er beter op mijn fritzing schema?

Dit is de feedback op mijn vragen.

- feedback 1: ldr herschakelen met mcp3008
- feedback 2: draden zoals SDA/SLC en TX RX mogen een andere kleur hebben
- feedback 3: proberen op schuine rechten eruit te halen



## Gesprek 2 (Datum: 24/25/2024)

Lector: Stijn Walcarius

Vragen voor dit gesprek:

- vraag 1: Is het database binnen de normen?

Dit is de feedback op mijn vragen.

- feedback 1: snelheid eruit -> geen berekening opslagen
- feedback 3: niet echt onderhoudsvriendelijk -> want dan moet een nieuwe tabel erbij komen wanneer nieuwe sensor erbij. maar gaat te moeilijk worden dus mag je gewoon zo laten. 
- feedback2 : Naamrit toevoegen -> wanneer je rit shared dan naam hebben voor de rit

## Gesprek 3 (Datum: 24/05/2024)

Lector: Geert Desloovere 

Vragen voor dit gesprek:

- [x] vraag 1:  Mag ik de (actuator) LED-strip veranderen door een 7*4 segment display om daarop mijn snelheid op af te spelen? Is het fritzing schema inorde?

Dit is de feedback op mijn vragen.

- feedback 1: Ja dat mag.
- feedback 2: Fritzing schema was nog niet ok : te weinig poorten om alles rechtstreeks aan te sluiten op de pi => lcd scherm geschakelt met pcf en 7*4 segment display geschakelt met shifterregister

## MV1 (Datum: 28/05/2024)

Lector: Geert Desloovere + Claudia Eeckhout + Dieter Roobrouck

Vragen voor dit gesprek:

- [x] vraag 1:  Geen vragen maar voorstellen van het project

Dit is de feedback op mijn vragen.

- feedback 1: op werkelijke website geen vakjargon gebruiken zoals  'ldr'  maar wel -> lichtwaarde
- feedback 2: snelheid halen uit gps sensor niet met mpu6050
- feedback 3: juiste rubrieken gebruiken op toggle 
- feedback 4: fritzing nog updaten /nog nieuw slot boeken voor fritzing na te kijken
- feedback 5: github nog in orde brengen volledig


## Gesprek 4 (Datum: 29/05/2024)

Lector: Pieter-Jan

Vragen voor dit gesprek:

- [x] vraag 1:  Is het fritzing schema inorde?
- [x] vraag 2:  Enige tips gevraagd over de chassis van het gps-tracker om het device zo klein mogelijk te krijgen?

Dit is de feedback op mijn vragen.

- feedback 1: Fritzing is in het algemeen wel inorde. De MPU component is niet duidelijk op het schema en moet een postage komen met meer verduidelijking. De veiligheidweerstand op de knop moet 470 ohm zijn in plaats van 220hm. De weerstand die geschakelt is op de LDR moet 10k ohm zijn. De draden op het breadbord schema mochten rechter staan. De draden op het schema mogen niet over andere componenten geplaatst worden. Draden die naar dezelfde pinnen moeten (parrallel geschakelt) mochten dezelfde kleur hebben voor de duidelijkheid.
- feedback 2: Gebruik van persplaat pcb om geen breadbord te gebruiken die veel plaats inneemt. Zo'n pcb persplaat is ook een goeie oplossing voor de  pcf en accelerator omdat die parallel geschakelt moeten worden op de I2C bus. 