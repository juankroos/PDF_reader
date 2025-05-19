
class Pdf(Basemodel):
    """
    Class to handle PDF files.
    """
    path : str
    title : str
    author : str
    date : datetime
    size : int
    creator : str
    page_count : int
    current_page : int


    def __init__(self, file_path):
        """
        Initialize the Pdf object with the file path.
        """
        self.path = path
        self.title = None
        self.author = None
        self.date = None
        self.size = None  # taille en octets
        self.creator = None
        self.page_count = None
        self.current_page = 0  # page actuelle (index 0 = page 1)
        self.doc = None  # document PyMuPDF, chargé par LoadPDF
        self.load_metadata()

    def load_metadata(self):
        """charge les métadonnées du PDF."""
        try:
            with fitz.open(self.path) as doc:
                info = doc.metadata
                self.title = info.get("title", "Inconnu")
                self.author = info.get("author", "Inconnu")
                self.date = info.get("creationDate", "Inconnu")
                self.creator = info.get("creator", "Inconnu")
                self.page_count = len(doc)
                self.size = os.path.getsize(self.path)
        except Exception as e:
            print(f"Erreur lors du chargement des métadonnées : {e}")

    def load_pdf(self):
        """ouvre le document PDF"""
        if self.doc is None:
            try:
                self.doc = fitz.open(self.path)
            except Exception as e:
                print(f"Erreur lors du chargement du PDF : {e}")
                self.doc = None
        return self.doc is not None

    def close_pdf(self):
        """ferme le document PDF"""
        if self.doc is not None:
            self.doc.close()
            self.doc = None


    def page_skip(self, page_number):
        """change la page actuelle et renvoie une image pour l'affichage."""
        if not self.load_pdf():
            return None
        # vérifie si le numéro de page est valide
        if not (0 <= page_number < self.page_count):
            print(f"Page {page_number + 1} hors limites (1-{self.page_count})")
            return None
        try:
            self.current_page = page_number # recupere la page actuelle
            page = self.doc.load_page(page_number)  # charge la page
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # rendu avec zoom x2
            return pix  # renvoie l'image pour le front-end
        except Exception as e:
            print(f"Erreur lors du changement de page : {e}")
            return None

    def search_text(self, text):
        """recherche un texte dans la page actuelle et renvoie les zones trouvées."""
        if not self.load_pdf() or self.current_page is None:
            print("Aucun document ou page chargée")
            return []
        try:
            page = self.doc.load_page(self.current_page)
            areas = page.search_for(text)  # recherche le texte
            return areas  # liste de rectangles (zones où le texte est trouvé)
        except Exception as e:
            print(f"Erreur lors de la recherche : {e}")
            return []
'''
class Word(MethodFIle):
    def __init__(self, path):
        """Initialise un objet PDFFile."""
        self.path = path
        self.title = None
        self.author = None
        self.date = None
        self.size = None  # taille en octets
        self.creator = None
        self.page_count = None
        self.current_page = 0  # page actuelle (index 0 = page 1)
        self.doc = None

        def load_pdf(self):
'''

