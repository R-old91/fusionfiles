import streamlit as st
import pandas as pd
import zipfile
import tempfile
import os

st.set_page_config(page_title="Fusion CSV", page_icon="📊")
st.title("📁 Amélie script")

# Upload d’un fichier zip
uploaded_zip = st.file_uploader("Téléverse un dossier compressé (.zip) contenant des fichiers .csv", type="zip")

if uploaded_zip:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Sauvegarder temporairement le zip
        zip_path = os.path.join(tmpdir, "fichiers.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        # Extraction
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        # Récupération des fichiers .csv extraits
        csv_files = [
            os.path.join(root, f)
            for root, _, files in os.walk(tmpdir)
            for f in files
            if f.endswith('.csv')
        ]

        if not csv_files:
            st.error("Aucun fichier .csv trouvé dans le zip.")
        else:
            # Fusion
            dfs = []
            for file in csv_files:
                try:
                    dfs.append(pd.read_csv(file))
                except Exception as e:
                    st.warning(f"Erreur lors de la lecture de {file} : {e}")
            if dfs:
                all_data = pd.concat(dfs, ignore_index=True)

                # Sauvegarde
                output_file = os.path.join(tmpdir, "fichier_fusionne.csv")
                all_data.to_csv(output_file, index=False)

                # Téléchargement
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📥 Télécharger le fichier fusionné",
                        data=f,
                        file_name="fichier_fusionne.csv",
                        mime="text/csv"
                    )
            else:
                st.error("Impossible de lire les fichiers CSV.")
