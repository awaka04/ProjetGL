import unittest
from datetime import datetime
from main import (Projet, Membre, Tache, Equipe, Jalon, Risque, Changement,
                  EmailNotificationStrategy, NotificationContext)

class TestProjet(unittest.TestCase):

    def setUp(self):
        self.notification_strategy = EmailNotificationStrategy()
        self.notification_context = NotificationContext(self.notification_strategy)
        self.projet = Projet(
            nom="MQP",
            description="Mesure Qualité et Performance Logicielle",
            date_debut=datetime(2024, 5, 30),
            date_fin=datetime(2024, 6, 5),
            notification_context=self.notification_context

        )
        self.membre1 = Membre("Ndeye coumba", "Chef de projet")

        self.membre2 = Membre("Awa", "Directeur General")

        self.projet.ajouter_membre_equipe(self.membre1)
        self.projet.ajouter_membre_equipe(self.membre2)

    def test_ajouter_tache(self):
        tache1 = Tache(
            nom="PartieA",
            description="Classes Principales ",
            date_debut=datetime(2024, 5, 30),
            date_fin=datetime(2024, 6, 5),
            responsable=self.membre1,
            statut="En cours"


        )
        self.projet.ajouter_tache(tache1)
        self.assertIn(tache1, self.projet.taches)

    def test_definir_budget(self):
        self.projet.definir_budget(150000.0)
        self.assertEqual(self.projet.budget, 150000.0)

    def test_ajouter_risque(self):
        risque1 = Risque("Risque 1", 0.3, "Élevé")
        self.projet.ajouter_risque(risque1)
        self.assertIn(risque1, self.projet.risques)

    def test_ajouter_jalon(self):
        jalon1 = Jalon("Jalon 1", "2024-06-01")
        self.projet.ajouter_jalon(jalon1)
        self.assertIn(jalon1, self.projet.jalons)

    def test_enregistrer_changement(self):
        self.projet.enregistrer_changement("Modifier le nom du projet")
        self.assertEqual(len(self.projet.changements), 1)

    def test_generer_rapport_performance(self):
        rapport = self.projet.generer_rapport_performance()
        self.assertIn("rapport", rapport)

if __name__ == '__main__':
    unittest.main()
