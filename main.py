from datetime import datetime
from typing import List, Optional


# l'interface NotificationStrategy
class NotificationStrategy:
    def envoyer(self, message: str, destinataire: "Membre"):
        raise NotImplementedError(
            "Cette méthode doit être implémentée par une sous-classe"
        )


# L'implementation de la classe EmailNotificationStrategy
class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: "Membre"):
        print(f"Notification envoyée à {destinataire.nom} par email: {message}")


# L'implementation de la classe SMSNotificationStrategy
class SMSNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: "Membre"):
        print(f"Notification envoyée à {destinataire.nom} par SMS: {message}")


# Classe NotificationContext
class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notify(self, message: str, destinataires: List["Membre"]):
        if self.strategy:
            for destinataire in destinataires:
                self.strategy.envoyer(message, destinataire)


# Classe Membre
class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role

    def __str__(self):
        return f"{self.nom} ({self.role})"


# Classe Tache
class Tache:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = []

    def ajouter_dependance(self, tache: "Tache"):
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        self.statut = statut


# Classe Equipe
class Equipe:
    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        return self.membres


# Classe Jalon
class Jalon:
    def __init__(self, nom: str, date: str):
        self.nom = nom
        self.date = datetime.strptime(date, "%Y-%m-%d")


# Classe Risque
class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


# Classe Changement
class Changement:
    def __init__(self, description: str, version: int):
        self.description = description
        self.version = version
        self.date = datetime.now()


# Classe Projet
class Projet:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        notification_context: NotificationContext,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.taches = []
        self.equipe = Equipe()
        self.budget = 0.0
        self.risques = []
        self.jalons = []
        self.version = 1.0
        self.changements = []
        self.chemin_critique = []
        self.notification_context = notification_context

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context.strategy = strategy

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(
            f"Nouvelle tâche ajoutée: {tache.nom}", self.equipe.obtenir_membres()
        )

    def ajouter_membre_equipe(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe", [membre])

    def definir_budget(self, budget: float):
        self.budget = budget
        self.notifier(
            f"Le budget du projet a été défini à {budget} Unité Monétaire",
            self.equipe.obtenir_membres(),
        )

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(
            f"Nouveau risque ajouté: {risque.description}",
            self.equipe.obtenir_membres(),
        )

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(
            f"Nouveau jalon ajouté: {jalon.nom}", self.equipe.obtenir_membres()
        )

    def enregistrer_changement(self, description: str):
        changement = Changement(description, self.version)
        self.changements.append(changement)
        self.version += 0.1
        self.notifier(
            f"Changement enregistré: {description} (version {self.version})",
            self.equipe.obtenir_membres(),
        )

    def generer_rapport_performance(self) -> str:
        rapport = f"Projet: {self.nom}\nDescription: {self.description}\nBudget: {self.budget}\nVersion: {self.version}\n"
        rapport += f"Tâches: {len(self.taches)}\nÉquipe: {len(self.equipe.obtenir_membres())} membres\nRisques: {len(self.risques)}\n"
        rapport += f"Jalons: {len(self.jalons)}\nChangements enregistrés: {len(self.changements)}\n"
        return rapport

    def calculer_chemin_critique(self):
        # Méthode simplifiée pour calculer le chemin critique (peut nécessiter des détails supplémentaires)
        self.chemin_critique = []  # Logique pour calculer le chemin critique

    def notifier(self, message: str, destinataires: List[Membre]):
        self.notification_context.notify(message, destinataires)


# Exemple d'utilisation:
if __name__ == "__main__":
    notification_strategy = EmailNotificationStrategy()
    notification_context = NotificationContext(notification_strategy)

    projet = Projet(
        nom="MQP",
        description="Mesure Qualité et Performance Logicielle",
        date_debut=datetime.now(),
        date_fin=datetime(2024, 12, 31),
        notification_context=notification_context,
    )

    # Ajouter des taches, membres, etc.
    membre1 = Membre("Ndeye coumba", "Chef de projet")

    membre2 = Membre("Awa", "Directeur General")

    tache1 = Tache(
        nom="PartieA",
        description="Classes Principales ",
        date_debut=datetime.now(),
        date_fin=datetime(2024, 6, 5),
        responsable=membre1,
        statut="En cours",
    )
    tache2 = Tache(
        nom="PartieB",
        description="Test, Mesure et Qualité du code",
        date_debut=datetime.now(),
        date_fin=datetime(2024, 6, 5),
        responsable=membre2,
        statut="En cours",
    )
    projet.ajouter_tache(tache1)
    projet.ajouter_tache(tache2)

    # Ajouter une dépendance à la tâche
    tache_dependance = Tache(
        nom="Tâche Dépendante",
        description="Description de la tâche dépendante",
        date_debut=datetime.now(),
        date_fin=datetime(2024, 5, 1),
        responsable=membre1,
        statut="En cours",
    )
    tache1.ajouter_dependance(tache_dependance)

    # Ajouter un membre à l'équipe
    projet.ajouter_membre_equipe(membre1)
    projet.ajouter_membre_equipe(membre2)

    # Définir un budget
    projet.definir_budget(150000.0)

    # Ajouter un risque
    risque1 = Risque("Risque 1", 0.3, "Élevé")
    projet.ajouter_risque(risque1)

    # Ajouter un jalon
    jalon1 = Jalon("Jalon 1", "2024-06-01")
    projet.ajouter_jalon(jalon1)

    # Enregistrer un changement
    projet.enregistrer_changement("Modifier le nom du projet")

    # Générer un rapport de performance
    rapport = projet.generer_rapport_performance()
    print(rapport)

    # Notifier des membres
    projet.notifier("bonjour, comment allez-vous?", [membre1])
    projet.notifier("bonjour, ce message est important", [membre2])
