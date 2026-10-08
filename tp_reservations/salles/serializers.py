"""Tache 1 et 2 : serializers et validation.

A FAIRE :
  - SalleSerializer (ModelSerializer)
  - ReservationSerializer (ModelSerializer) :
      * le champ `utilisateur` est en LECTURE SEULE (il sera renseigne par la vue)
      * validation : `fin` strictement apres `debut`
      * validation : pas de chevauchement avec une autre reservation CONFIRMEE
        de la meme salle
"""
from rest_framework import serializers

from .models import Reservation, Salle  # noqa: F401  (a utiliser)

class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ['nom', 'capacite', 'batiment']
    

class ReservationSerializer(serializers.ModelSerializer):

    utilisateur = serializers.ReadOnlyField(source='utilisateur.username')

    class Meta:
        model = Reservation
        fields = ['salle', 'date_debut', 'date_fin', 'motif', 'statut', 'cree_le']

    def validate(self, data):
        if 'salle' in data:
            salle = data['salle']
        elif self.instance:
            salle = self.instance.salle
        else:
            raise serializers.ValidationError("La salle est UN CHAMPS obligatoire.")
        
        if 'date_debut' in data:
            date_debut = data['date_debut']
        elif self.instance:
            date_debut = self.instance.date_debut
        else:
            raise serializers.ValidationError("La date de début est UN CHAMPS obligatoire.")

        if 'date_fin' in data:
            date_fin = data['date_fin']
        elif self.instance:
            date_fin = self.instance.date_fin
        else:
            raise serializers.ValidationError("La date de fin est UN CHAMPS obligatoire.")

        if 'statut' in data:
            statut = data['statut']
        elif self.instance:
            statut = self.instance.statut
        else:
            statut = 'CONFIRMEE'

        if date_debut >= date_fin:
            raise serializers.ValidationError("La date de début doit être inferieure à la date de fin.")

        if statut == 'ANNULEE':
            return data

        reservations_existantes = Reservation.objects.filter(salle=salle)
        
        reservations_existantes = reservations_existantes.exclude(statut='ANNULEE')

        if self.instance:
            reservations_existantes = reservations_existantes.exclude(id=self.instance.id)

        if reservations_existantes.exists():
            raise serializers.ValidationError("La salle est déjà réservée pour cet horaire.")

        return data