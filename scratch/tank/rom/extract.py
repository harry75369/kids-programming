from PIL import Image

colorPalletes = {
        "tank_a": [(0,0,0),(104,104,0),(231,156,33),(231,231,148)],
        "tank_b": [(0,0,0),(0,75,84),(182,182,182),(255,255,255)],
        "wall": [(0,0,0),(166,84,0),(118,7,0),(110,110,110)],
        "solid": [(0,0,0),(110,110,110),(182,182,182),(255,255,255)],
        "grass": [(0,0,0),(150,219,0),(6,84,0),(0,93,6)],
        "boom": [(0,0,0),(101,0,134),(189,56,36),(255,255,255)]
}

class NESRom:

    def __init__(self, fileName, pallete):
        blob = open(fileName).read()
        self.szHeader = 16
        self.nPRG = ord(blob[4])
        self.nCHR = ord(blob[5])
        self.szPRG = 16384
        self.szCHR = 8192
        self.nSpritePerCHR = 512
        self.szSprite = self.szCHR / self.nSpritePerCHR
        self.szTile = 8
        self.scale = 4
        self.PRGs = [blob[self.szHeader:][(i*self.szPRG):((i+1)*self.szPRG)] for i in range(self.nPRG)]
        self.CHRs = [blob[(self.szHeader+self.szPRG*self.nPRG):][(i*self.szCHR):((i+1)*self.szCHR)] for i in range(self.nCHR)]
        self.colorPallete = pallete

    def makeTileMatrix(self, channel):
        matrix = []
        for rowByte in channel:
            binString = bin(ord(rowByte))[2:]
            l = len(binString)
            binString = '0' * (8-l) + binString
            matrix.append(map(int, binString))
        return matrix

    def makeSpriteImage(self, blob):
        img = Image.new('RGB', (self.szTile, self.szTile))
        pixels = img.load()
        channelA = self.makeTileMatrix(blob[0:self.szSprite/2])
        channelB = self.makeTileMatrix(blob[self.szSprite/2:self.szSprite])
        for i in range(self.szTile):
            for j in range(self.szTile):
                colorIdx = channelA[i][j] + 2*channelB[i][j]
                pixels[j,i] = self.colorPallete[colorIdx]
        return img.resize((self.scale*self.szTile, self.scale*self.szTile))

    def sprites(self):
        _sprites = []
        for CHR in self.CHRs:
            for i in range(self.nSpritePerCHR):
                s = CHR[(i*self.szSprite):((i+1)*self.szSprite)]
                _sprites.append(self.makeSpriteImage(s))
        return _sprites

    def combinedSprites(self):
        _combined = []
        sprites = self.sprites()
        sz = self.szTile * self.scale
        for i in range(len(sprites)/4):
            c = Image.new('RGB', (sz*2, sz*2))
            c.paste(sprites[i*4], (0, 0))
            c.paste(sprites[i*4+1], (0, sz))
            c.paste(sprites[i*4+2], (sz, 0))
            c.paste(sprites[i*4+3], (sz, sz))
            _combined.append(c)
        return _combined

    def allSprites(self):
        sprites = self.combinedSprites()
        nSpritePerRow = 8
        nRow = len(sprites) / nSpritePerRow
        sz = self.szTile * self.scale * 2
        allS = Image.new('RGB', (sz*nSpritePerRow, sz*nRow))
        for i in range(nRow):
            for j in range(nSpritePerRow):
                allS.paste(sprites[i*nSpritePerRow+j], (j*sz, i*sz))
        return allS

for (name, pallete) in colorPalletes.items():
    rom = NESRom("./BATLCITY.NES", pallete)
    sprites = rom.allSprites()
    sprites.save(name+".bmp")

