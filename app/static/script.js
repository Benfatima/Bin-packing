// script.js
document.addEventListener('DOMContentLoaded', function () {
    var taillePopulationContainer = document.getElementById('taillePopulationContainer');
    var nbrGenerationsContainer = document.getElementById('nbrGenerationsContainer');
    var tauxMutationContainer = document.getElementById('tauxMutationContainer');
    var nbrLoupsContainer = document.getElementById('nbrLoupsContainer');
    var nbrIterationsContainer = document.getElementById('nbrIterationsContainer');

    var radioButtons = document.querySelectorAll('input[name="algorithme"]');
    
    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener('change', function () {
            if (this.value === 'genetique') {
                // Afficher les champs spécifiques à l'algorithme génétique
                taillePopulationContainer.style.display = 'flex';
                nbrGenerationsContainer.style.display = 'flex';
                tauxMutationContainer.style.display = 'flex';
                nbrLoupsContainer.style.display = 'none';
                nbrIterationsContainer.style.display = 'none';
            } else if (this.value === 'loupsgris') {
                // Afficher les champs spécifiques à l'algorithme des loups gris
                taillePopulationContainer.style.display = 'none';
                nbrGenerationsContainer.style.display = 'none';
                tauxMutationContainer.style.display = 'none';
                nbrLoupsContainer.style.display = 'flex';
                nbrIterationsContainer.style.display = 'flex';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Récupérer le bouton et ajouter un gestionnaire d'événements
    const commencerBtn = document.getElementById('commencerBtn');
    commencerBtn.addEventListener('click', function () {
        // Récupérer les valeurs des champs
        const nombreObjets = document.getElementById('nbr_objets').value;
        const capaciteBin = document.getElementById('capacité-bin').value;
        const dimensionsObjets = document.getElementById('dimensions').value;


        // Récupérer la valeur de l'algorithme sélectionné
        const algorithmeSelectionne = document.querySelector('input[name="algorithme"]:checked').id;
        let parametres = {};
        if (algorithmeSelectionne === 'genetique') {
            parametres.taillePopulation = document.getElementById('Taille population').value;
            parametres.nbrGenerations = document.getElementById('Nombres générations').value;
            parametres.tauxMutation = document.getElementById('Taux mutation').value;
        } else if (algorithmeSelectionne === 'loupsgris') {
            parametres.nbrLoups = document.getElementById('Nombres loups').value;
            parametres.nbrIterations = document.getElementById('Nombres itérations').value;
        }
        else {
            console.error('Algorithme non pris en charge.');
            return;
        }

        fetch(`/run-algorithm/${algorithmeId}?nombreObjets=${nombreObjets}&capaciteBin=${capaciteBin}&dimensionsObjets=${dimensionsObjets}`, {
            method: 'POST', // ou 'GET' selon vos besoins
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(parametres),
        })
    .then(response => response.json())
    .then(resultat => {
        // Afficher les résultats dans votre structure HTML
        const nbrElement = document.querySelector('.nbr span');
        const affichage1Element = document.querySelector('.affichage1');

        nbrElement.textContent = resultat.nombre_boites_utilisees;

        // Vous devrez personnaliser cette partie selon le format de vos résultats
        // Par exemple, si resultat.solution contient un tableau de boîtes, vous pouvez le parcourir et l'afficher.
        resultat.solution.forEach((boite, index) => {
            const boiteDiv = document.createElement('div');
            boiteDiv.textContent = `Boîte ${index + 1}: ${boite.join(', ')}`;
            affichage1Element.appendChild(boiteDiv);
        });

        console.log(`Résultats de l'algorithme ${algorithmeSelectionne}:`, resultat);
    })
    .catch(error => console.error('Erreur lors de l\'appel API:', error));
    });

    // Autres fonctions, le cas échéant 
});
