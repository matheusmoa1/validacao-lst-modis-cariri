import ee

def initialize_gee():
    try:
        project_id = 'silken-apex-388004'  # ID do projeto
        ee.Initialize(project=project_id)
        print(f"Conectado ao Google Earth Engine com o projeto '{project_id}'.")
    except Exception as e:
        print("Autenticação necessária. Rodando ee.Authenticate()...")
        ee.Authenticate()
        ee.Initialize(project=project_id)
        print(f"Conectado ao Google Earth Engine com o projeto '{project_id}' após autenticação.")
