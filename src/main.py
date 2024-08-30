import pygame
from random import randint

class Hirvio:

  hirvio_lev = pygame.image.load("hirvio.png").get_width()
  hirvio_kor = pygame.image.load("hirvio.png").get_height()

  def __init__(self, x: int, y: int, tyyppi: int, nopeus: float) -> None:
    self.kuva = pygame.image.load("hirvio.png")
    self.rect = self.kuva.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.tyyppi = tyyppi
    self.nopeus = nopeus

  def piirra(self, naytto):
    naytto.blit(self.kuva, (self.rect.x, self.rect.y))

  def liiku(self, kohde):
    if self.tyyppi == 1:
      self.rect.y += self.nopeus
    if self.tyyppi == 2:
      self.rect.x += self.nopeus
    if self.tyyppi == 3:
      self.rect.y -= self.nopeus
    if self.tyyppi == 4:
      self.rect.x -= self.nopeus
    if self.tyyppi == 5:
      if self.rect.x > kohde.rect.x:
        self.rect.x -= self.nopeus
      if self.rect.x < kohde.rect.x:
        self.rect.x += self.nopeus
      if self.rect.y > kohde.rect.y:
        self.rect.y -= self.nopeus
      if self.rect.y < kohde.rect.y:
        self.rect.y += self.nopeus

class Kolikko:

  kolikko_lev = pygame.image.load("kolikko.png").get_width()
  kolikko_kor = pygame.image.load("kolikko.png").get_height()

  def __init__(self, x: int, y: int) -> None:
    self.kuva = pygame.image.load("kolikko.png")
    self.rect = self.kuva.get_rect()
    self.rect.x = x
    self.rect.y = y    

  def piirra(self, naytto):
    naytto.blit(self.kuva, (self.rect.x, self.rect.y))

class Robo:

  robo_lev = pygame.image.load("robo.png").get_width()
  robo_kor = pygame.image.load("robo.png").get_height()

  def __init__(self, x: int, y: int) -> None:
    self.kuva = pygame.image.load("robo.png")
    self.rect = self.kuva.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.vasemmalle = False
    self.oikealle = False
    self.ylos = False
    self.alas = False
    

  def piirra(self, naytto):
    naytto.blit(self.kuva, (self.rect.x, self.rect.y))

  def liikuta_oikealle(self, pelialue: tuple):
    if self.rect.x <= pelialue[1] - Robo.robo_lev:
      self.rect.x += 4

  def liikuta_vasemmalle(self, pelialue: tuple):
    if self.rect.x >= pelialue[0]:
      self.rect.x -= 4

  def liikuta_ylos(self, pelialue: tuple):
    if self.rect.y >= pelialue[0]:
      self.rect.y -= 4

  def liikuta_alas(self, pelialue: tuple):
    if self.rect.y <= pelialue[1] - Robo.robo_kor:
      self.rect.y += 4

class KerailyPeli:
  def __init__(self) -> None:
    pygame.init()

    self.leveys, self.korkeus = 1024, 768
    self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
    self.raja = 18
    self.pelialue = (self.raja, self.korkeus - self.raja)
    self.uusi_peli()

    self.otsikkofontti = pygame.font.SysFont("Arial", 32, bold=True)
    self.fontti = pygame.font.SysFont("Arial", 26, bold=True)

    pygame.display.set_caption("Keräilypeli")

    self.silmukka()

  def uusi_peli(self):
    self.kaynnissa = True
    self.pisteet = 0
    self.taso = 1
    self.taso_lapi = False
    self.peli_lapi = False
    self.peli_ohi = False
    self.robo = Robo(self.pelialue[1] / 2 - Robo.robo_lev / 2, self.pelialue[1] / 2 - Robo.robo_kor / 2)
    self.ohje_kolikko = Kolikko(785, 80)
    self.hirviot = []
    self.kolikot = []
    self.kello = pygame.time.Clock()

  def seuraava_taso(self):
    self.kaynnissa = True
    self.pisteet = 0
    self.taso += 1
    self.taso_lapi = False
    self.robo.x = self.pelialue[1] / 2 - Robo.robo_lev / 2
    self.robo.y = self.pelialue[1] / 2 - Robo.robo_kor / 2
    self.hirviot = []
    self.kolikot = []

  def silmukka(self):
    while True:
      self.tutki_tapahtumat()
      self.piirra_naytto()
      if self.kaynnissa:
        self.liiku()
        self.arvo_kolikko()
        self.arvo_hirvio()
        self.keraa_kolikko()
        self.tarkista_pisteet()

  def liiku(self):
    if self.robo.vasemmalle:
      self.robo.liikuta_vasemmalle(self.pelialue)
    if self.robo.oikealle:
      self.robo.liikuta_oikealle(self.pelialue)
    if self.robo.ylos:
      self.robo.liikuta_ylos(self.pelialue)
    if self.robo.alas:
      self.robo.liikuta_alas(self.pelialue)

  def tarkista_pisteet(self):
    if self.pisteet >= 10:
      if self.taso == 5:
        self.peli_lapi = True
      else:
        self.taso_lapi = True

  def arvo_kolikko(self):
    if len(self.kolikot) == 0:
      kolikko_x = randint(self.pelialue[0], self.pelialue[1] - Kolikko.kolikko_lev)
      kolikko_y = randint(self.pelialue[0], self.pelialue[1] - Kolikko.kolikko_kor)
      if self.onko_keratty(Kolikko(kolikko_x, kolikko_y)):
        return
      else:
        self.kolikot.append(Kolikko(kolikko_x, kolikko_y))

  def keraa_kolikko(self):
    for kolikko in self.kolikot:
      if self.onko_keratty(kolikko):
        self.kolikot.remove(kolikko)
        self.pisteet += 1

  def onko_keratty(self, kolikko: Kolikko):
    if self.robo.rect.colliderect(kolikko.rect):
      return True
    return False

  def arvo_hirvio(self):
    tyyppi = randint(1, self.taso)
    kohdat = [(randint(self.pelialue[0], self.pelialue[1] - Hirvio.hirvio_lev), -Hirvio.hirvio_kor),
              (-Hirvio.hirvio_lev, randint(self.pelialue[0], self.pelialue[1] - Hirvio.hirvio_kor)),
              (randint(self.pelialue[0], self.pelialue[1] - Hirvio.hirvio_lev), self.pelialue[1]),
              (self.pelialue[1], randint(self.pelialue[0], self.pelialue[1] - Hirvio.hirvio_kor))]
    nopeudet = [1, 2, 3, 4, 1]
    if tyyppi == 1 and randint(0, 90) < 1:
      self.hirviot.append(Hirvio(kohdat[0][0], kohdat[0][1], tyyppi, nopeudet[0]))
    if tyyppi == 2 and randint(0, 80) < 1:
      self.hirviot.append(Hirvio(kohdat[1][0], kohdat[1][1], tyyppi, nopeudet[1]))
    if tyyppi == 3 and randint(0, 70) < 1:
      self.hirviot.append(Hirvio(kohdat[2][0], kohdat[2][1], tyyppi, nopeudet[2]))
    if tyyppi == 4 and randint(0, 60) < 1:
      self.hirviot.append(Hirvio(kohdat[3][0], kohdat[3][1], tyyppi, nopeudet[3]))
    if tyyppi == 5 and randint(0, 50) < 1:
      arpa = randint(0, 3)
      self.hirviot.append(Hirvio(kohdat[arpa][0], kohdat[arpa][1], tyyppi, nopeudet[4]))

  def liikuta_hirvioita(self):
    if self.kaynnissa:
      for hirvio in self.hirviot:
        if hirvio.rect.x >= self.pelialue[0] - Hirvio.hirvio_lev and hirvio.rect.x <= self.pelialue[1] and\
        hirvio.rect.y >= self.pelialue[0] - Hirvio.hirvio_kor and hirvio.rect.y <= self.pelialue[1]:
          
          hirvio.piirra(self.naytto)
          
        hirvio.liiku(self.robo)
        self.tutki_tormaykset(hirvio)

  def tutki_tormaykset(self, hirvio: Hirvio):
    if self.robo.rect.colliderect(hirvio.rect):
        self.peli_ohi = True

  def piirra_naytto(self):
    self.naytto.fill("white")

    for kolikko in self.kolikot:
      kolikko.piirra(self.naytto)
    self.robo.piirra(self.naytto)
    self.liikuta_hirvioita()

    pygame.draw.rect(self.naytto, "red", (0, 0, self.pelialue[1] + self.raja, 
                                          self.pelialue[1] + self.raja), width=self.raja)
    pygame.draw.rect(self.naytto, "white", (self.pelialue[1] + self.raja, 0, 
                                            self.leveys - self.pelialue[1] + self.raja, self.korkeus))
    taso_teksti = self.otsikkofontti.render(f"TASO {self.taso}", True, "black")
    uusipeli_teksti = self.fontti.render(f"{"F5":8} Uusi peli", True, "black")
    lopeta_teksti = self.fontti.render(f"{"Esc":7} Sulje peli", True, "black")
    pisteet_teksti = self.otsikkofontti.render(f"{self.pisteet} / 10", True, "black")
    self.naytto.blit(taso_teksti, ((self.pelialue[1] + self.raja) + 65, 15))
    self.naytto.blit(uusipeli_teksti, ((self.pelialue[1] + self.raja) + 15, 675))
    self.naytto.blit(lopeta_teksti, ((self.pelialue[1] + self.raja) + 15, 720))
    self.naytto.blit(pisteet_teksti, (845, 82))
    self.ohje_kolikko.piirra(self.naytto)

    if self.peli_ohi:
      self.kaynnissa = False
      self.tyhjenna_pelialue()
      ohi_teksti = self.fontti.render(f"Peli päättyi! Selvisit tasolle {self.taso}.", True, "black")
      self.naytto.blit(ohi_teksti, ((self.pelialue[1] + self.raja) / 2 - ohi_teksti.get_width() / 2, 
                                    self.korkeus / 2 - ohi_teksti.get_height() / 2))
    if self.taso_lapi:
      self.kaynnissa = False
      self.tyhjenna_pelialue()
      tasolapi_teksti = self.fontti.render(f"Onnittelut! Läpäisit tason {self.taso}.", True, "black")
      jatka_teksti = self.fontti.render(f"Jatka seuraavalle tasolle painamalla Enter", True, "black")
      self.naytto.blit(tasolapi_teksti, ((self.pelialue[1] + self.raja) / 2 - 
                                         tasolapi_teksti.get_width() / 2, self.korkeus / 2 - 30))
      self.naytto.blit(jatka_teksti, ((self.pelialue[1] + self.raja) / 2 - 
                                      jatka_teksti.get_width() / 2, self.korkeus / 2 + 20))
      
    if self.peli_lapi:
      self.kaynnissa = False
      self.tyhjenna_pelialue()
      pelilapi_teksti = self.fontti.render(f"Onneksi olkoon, pääsit pelin läpi!", True, "black")
      self.naytto.blit(pelilapi_teksti, ((self.pelialue[1] + self.raja) / 2 - pelilapi_teksti.get_width() / 2,
                                         self.korkeus / 2 - pelilapi_teksti.get_height() / 2))

    pygame.display.flip()
    self.kello.tick(30)

  def tyhjenna_pelialue(self):
    pygame.draw.rect(self.naytto, "white", (self.raja, self.raja, self.pelialue[1] - 
                                              self.raja, self.pelialue[1] - self.raja))

  def tutki_tapahtumat(self):
    for tapahtuma in pygame.event.get():
      if tapahtuma.type == pygame.QUIT:
        exit()
      if tapahtuma.type == pygame.KEYDOWN:
        if tapahtuma.key == pygame.K_LEFT:
          self.robo.vasemmalle = True
        if tapahtuma.key == pygame.K_RIGHT:
          self.robo.oikealle = True
        if tapahtuma.key == pygame.K_UP:
          self.robo.ylos = True
        if tapahtuma.key == pygame.K_DOWN:
          self.robo.alas = True
        if tapahtuma.key == pygame.K_ESCAPE:
          exit()
        if tapahtuma.key == pygame.K_F5:
          self.uusi_peli()
        if tapahtuma.key == pygame.K_RETURN or tapahtuma.key == pygame.K_KP_ENTER:
          if self.taso_lapi:
            self.seuraava_taso()

      if tapahtuma.type == pygame.KEYUP:
        if tapahtuma.key == pygame.K_LEFT:
          self.robo.vasemmalle = False
        if tapahtuma.key == pygame.K_RIGHT:
          self.robo.oikealle = False
        if tapahtuma.key == pygame.K_UP:
          self.robo.ylos = False
        if tapahtuma.key == pygame.K_DOWN:
          self.robo.alas = False

if __name__ == "__main__":
  KerailyPeli()