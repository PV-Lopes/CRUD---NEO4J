from neo4j import GraphDatabase

# Configurações de conexão(Credenciais)

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "123456"

class Neo4jCRUD:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_person(self, name, age):
        with self.driver.session() as session:
            session.run(
                "CREATE (p:Person {name: $name, age: $age})",
                name=name, age=age
            )
            print(f"Pessoa '{name}' criada com sucesso.")

    def read_person(self, name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person {name: $name}) RETURN p.name AS name, p.age AS age",
                name=name
            )
            record = result.single()
            if record:
                print(f"Nome: {record['name']}, Idade: {record['age']}")
            else:
                print(f"Nenhuma pessoa encontrada com o nome '{name}'.")

    def update_person(self, name, new_age):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person {name: $name}) SET p.age = $age RETURN p",
                name=name, age=new_age
            )
            if result.single():
                print(f"Pessoa '{name}' atualizada para idade {new_age}.")
            else:
                print(f"Nenhuma pessoa encontrada com o nome '{name}'.")

    def delete_person(self, name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person {name: $name}) DETACH DELETE p",
                name=name
            )
            print(f"Pessoa '{name}' deletada (se existia).")

    def list_all(self):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p.name AS name, p.age AS age")
            print("Pessoas cadastradas:")
            for record in result:
                print(f" - {record['name']} (Idade: {record['age']})")

# MENU
def menu():
    db = Neo4jCRUD(URI, USER, PASSWORD)

    while True:
        print("\n=== MENU - CRUD com Neo4j ===")
        print("1 - Criar pessoa")
        print("2 - Buscar pessoa")
        print("3 - Atualizar idade")
        print("4 - Deletar pessoa")
        print("5 - Listar todas as pessoas")
        print("0 - Sair")

        op = input("Escolha uma opção: ")

        if op == "1":
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            db.create_person(nome, idade)

        elif op == "2":
            nome = input("Nome a buscar: ")
            db.read_person(nome)

        elif op == "3":
            nome = input("Nome: ")
            nova_idade = int(input("Nova idade: "))
            db.update_person(nome, nova_idade)

        elif op == "4":
            nome = input("Nome a deletar: ")
            db.delete_person(nome)

        elif op == "5":
            db.list_all()

        elif op == "0":
            db.close()
            print("Encerrando...")
            break

        else:
            print("Opção inválida, tente novamente.")

# Executa o menu
if __name__ == "__main__":
    menu()
