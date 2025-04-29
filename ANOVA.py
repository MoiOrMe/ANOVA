import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Charger le fichier Excel (adapte le chemin si besoin)
df = pd.read_excel("Data_IHM.xlsx")  # ton fichier doit avoir les colonnes : Participant, Mode d'interaction, Temps de complétion (s)

# Renommer les colonnes pour simplifier le code (facultatif)
df = df.rename(columns={
    "Mode d'interaction": "Mode",
    "Temps de complétion (s)": "Temps",
    "Nombre d'erreurs" : "Erreurs",
    "Facilité d'utilisation" : "Facilite",
    "Efficacité perçue" : "Efficacite", 
    "Confort" : "Confort"
})

def analyse_satisfaction(df, critere):
    
    model = ols(f'{critere} ~ C(Mode)', data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)
    print(f"\n=== ANOVA sur {critere} ===")
    print(anova)

    print(f"\n=== Test de Tukey pour {critere} ===")
    tukey = pairwise_tukeyhsd(endog=df[critere],
                              groups=df['Mode'],
                              alpha=0.05)
    print(tukey)

# --- ANOVA sur les temps de complétion ---
model = ols('Temps ~ C(Mode)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("=== ANOVA sur le temps de complétion ===")
print(anova_table)

# --- Test de Tukey si ANOVA significative ---
print("\n=== Test de Tukey ===")
tukey = pairwise_tukeyhsd(endog=df['Temps'],
                          groups=df['Mode'],
                          alpha=0.05)
print(tukey)


# --- ANOVA sur les erreurs ---
model_err = ols('Erreurs ~ C(Mode)', data=df).fit()
anova_err = sm.stats.anova_lm(model_err, typ=2)
print("\n=== ANOVA sur les erreurs ===")
print(anova_err)

# --- Test de Tukey pour les erreurs ---
print("\n=== Test de Tukey (erreurs) ===")
tukey_err = pairwise_tukeyhsd(endog=df['Erreurs'],
                              groups=df['Mode'],
                              alpha=0.05)
print(tukey_err)

# Lancer pour chaque critère
for critere in ["Facilite", "Efficacite", "Confort"]:
    analyse_satisfaction(df, critere)