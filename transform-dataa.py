import pdfplumber
import pandas as pd
import zipfile
import os

pdf_path = "/home/rabbitnuna/Studies/webS/anexos/Anexo_I..pdf"

def extract_table(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        tabelas = []
        for pagina in pdf.pages:
            tabela = pagina.extract_table()
            if tabela:
                tabelas.extend(tabela)
        return tabelas

def transform_data(data):
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data[1:], columns=data[0])
    df.replace({"OD": "Odontológico", "AMB": "Ambulatorial"}, inplace=True)
    return df

def save(df, filename):
    csv_file = f"{filename}.csv"
    zip_file = f"{filename}.zip"

    df.to_csv(csv_file, index=False, encoding='utf-8')
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_file)
    os.remove(csv_file)
    print(f"Salvo como {zip_file}")

data = extract_table(pdf_path)

if data:
    save(transform_data(data), "resultado")
else:
    print("Erro!")
