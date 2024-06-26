import tkinter as tk
import tkinter.ttk as ttk
import json
import time
import threading

class TarefaProcesso:
    def __init__(self, nome, pid, ppid, memoria, cpu, leitura, escrita):
        self.nome = nome
        self.pid = pid
        self.ppid = ppid
        self.memoria = memoria
        self.cpu = cpu
        self.leitura = leitura
        self.escrita = escrita
        


class TarefaMemoria:
    def __init__(self, nome, pid, total_memory, code_memory, heap_memory, stack_memory, total_pages, code_pages, heap_pages, stack_pages):
        self.nome = nome
        self.pid = pid
        self.total_memory = total_memory
        self.code_memory = code_memory
        self.heap_memory = heap_memory
        self.stack_memory = stack_memory
        self.total_pages = total_pages
        self.code_pages = code_pages
        self.heap_pages = heap_pages
        self.stack_pages = stack_pages

class TarefaGlobal:
    def __init__(self, total_ram, free_ram, ram_usage_percentage, total_swap, free_swap, swap_usage_percentage):
        self.total_ram = total_ram
        self.free_ram = free_ram
        self.ram_usage_percentage = ram_usage_percentage
        self.total_swap = total_swap
        self.free_swap = free_swap
        self.swap_usage_percentage = swap_usage_percentage

class GerenciadorTarefas:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gerenciador de Tarefas")
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill=tk.BOTH)

                # Criando as abas para cada tabela
        self.tab_processos = ttk.Frame(self.notebook)
        self.tab_memoria = ttk.Frame(self.notebook)
        self.tab_global = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_processos, text="Processos")
        self.notebook.add(self.tab_memoria, text="Memória")
        self.notebook.add(self.tab_global, text="Global")

 
        # Criar tabela_processos de tarefas
        self.tabela_processos = ttk.Treeview(self.tab_processos, columns=("Nome","PID", "PPID", "Memória", "CPU", "Leitura", "Escrita"))
        self.tabela_processos.heading("Nome", text="Nome")
        self.tabela_processos.heading("PID", text="PID")
        self.tabela_processos.heading("PPID", text="PPID")
        self.tabela_processos.heading("Memória", text="Memória")
        self.tabela_processos.heading("CPU", text="CPU")
        self.tabela_processos.heading("Leitura", text="Leitura")
        self.tabela_processos.heading("Escrita", text="Escrita")
        self.tabela_processos.pack(expand=True, fill=tk.BOTH, side="top")
        
        self.tabela_memoria = ttk.Treeview(self.tab_memoria, columns=("Nome", "PID", "Memoria Total", "Memoria Codigo", "Memoria Heap", "Memoria Stack",
                                                                 "Total de Paginas", "Paginas Codigos", "Paginas Heap", "Paginas Stack"))
        self.tabela_memoria.heading("Nome", text="Nome")
        self.tabela_memoria.heading("PID", text="PID")
        self.tabela_memoria.heading("Memoria Total", text="Memoria Total")
        self.tabela_memoria.heading("Memoria Codigo", text="Memoria Codigo")
        self.tabela_memoria.heading("Memoria Heap", text="Memoria Heap")
        self.tabela_memoria.heading("Memoria Stack", text="Memoria Stack")
        self.tabela_memoria.heading("Total de Paginas", text="Total de Paginas")
        self.tabela_memoria.heading("Paginas Codigos", text="Paginas Codigos")
        self.tabela_memoria.heading("Paginas Heap", text="Paginas Heap")
        self.tabela_memoria.heading("Paginas Stack", text="Paginas Stack")
        self.tabela_memoria.pack(expand=True, fill=tk.BOTH, side="top")
        
        self.tabela_global = ttk.Treeview(self.tab_global, columns=("RAM Total", "RAM Livre", "Porcentagem de RAM utilizada", "Swap Total", 
                                                                "Swap Livre", "Porcentagem de Swap utilizado"))
        self.tabela_global.heading("RAM Total", text="RAM Total")
        self.tabela_global.heading("RAM Livre", text="RAM Livre")
        self.tabela_global.heading("Porcentagem de RAM utilizada", text="Porcentagem de RAM utilizada")
        self.tabela_global.heading("Swap Total", text="Swap Total")
        self.tabela_global.heading("Swap Livre", text="Swap Livre")
        self.tabela_global.heading("Porcentagem de Swap utilizado", text="Porcentagem de Swap utilizado")
        self.tabela_global.pack(expand=True, fill=tk.BOTH, side="top")


        # Carregar tarefas iniciais
        self.carregar_tarefas_processos()
        self.carregar_tarefas_memoria()
        self.carregar_tarefas_global()

        # Iniciar thread de atualização automática
        self.atualizar_thread = threading.Thread(target=self.atualizar_tarefas_automaticamente)
        self.atualizar_thread.start()

        # Executar loop principal da interface
        self.window.mainloop()

    def limpar_tabela_processos(self):
        self.tabela_processos.delete(*self.tabela_processos.get_children())
    
    def limpar_tabela_memoria(self):
        self.tabela_processos.delete(*self.tabela_memoria.get_children())

    def limpar_tabela_global(self):
        self.tabela_processos.delete(*self.tabela_global.get_children())

    def carregar_tarefas_processos(self):
        with open("api\processes.json", "r") as arquivo:
            dados = json.load(arquivo)

        tarefas_processos = []
        for tarefa in dados:
            nome = tarefa["name"]
            pid = tarefa["pid"]
            ppid = tarefa["ppid"]
            memoria = str(tarefa["mem_usage_mb"]) + " Mb"
            cpu = str(tarefa["cpu_usage"]) + "%"
            leitura = str(tarefa["total_read_bytes"]) + " b"
            escrita = str(tarefa["total_write_bytes"]) + " b"

            nova_tarefa = TarefaProcesso(nome, pid, ppid, memoria, cpu, leitura, escrita)
            tarefas_processos.append(nova_tarefa)
        
        self.limpar_tabela_processos()
        for tarefa in tarefas_processos:
                self.inserir_tarefa_processo(tarefa)
    
    def carregar_tarefas_memoria(self):
        with open("api\processes_memory.json", "r") as arquivo:
            dados = json.load(arquivo)
        tarefas_memoria = []
        for tarefa in dados:
            nome = tarefa["name"]
            pid = tarefa["pid"]
            total_memory = tarefa["total_memory"]
            code_memory = tarefa["code_memory"]
            heap_memory = tarefa["heap_memory"]
            stack_memory = tarefa["stack_memory"]
            total_pages = tarefa["total_pages"]
            code_pages = tarefa["code_pages"]
            heap_pages = tarefa["heap_pages"]
            stack_pages = tarefa["stack_pages"]
            nova_tarefa = TarefaMemoria(nome, pid, total_memory, code_memory, heap_memory, stack_memory, total_pages, code_pages, heap_pages, stack_pages)
            tarefas_memoria.append(nova_tarefa)


        self.limpar_tabela_memoria()
        for tarefa in tarefas_memoria:
            self.inserir_tarefa_memoria(tarefa)

    def carregar_tarefas_global(self):
        with open("api\global_data.json", "r") as arquivo:
            dados = json.load(arquivo)

        tarefas_global = []
        total_ram = str(dados["total_ram"]) + " Mb"
        free_ram = str(dados["free_ram"]) + " Mb"
        ram_usage_percentage = str(dados["ram_usage_percentage"]) + " %"
        total_swap = str(dados["total_swap"]) + " Mb"
        free_swap = str(dados["free_swap"]) + " Mb"
        swap_usage_percentage = str(dados["swap_usage_percentage"]) + " %"
        nova_tarefa = TarefaGlobal(total_ram, free_ram, ram_usage_percentage, total_swap, free_swap, swap_usage_percentage)
        tarefas_global.append(nova_tarefa)
        
        self.limpar_tabela_global()
        for tarefa in tarefas_global:
                self.inserir_tarefa_global(tarefa)
    

    def inserir_tarefa_processo(self, tarefa):
        valores = (tarefa.nome, tarefa.pid, tarefa.ppid, tarefa.memoria, tarefa.cpu, tarefa.leitura, tarefa.escrita)
        self.tabela_processos.insert("", tk.END, values=valores)
    
    def inserir_tarefa_memoria(self, tarefa):
        valores = (tarefa.nome, tarefa.pid, tarefa.total_memory, tarefa.code_memory, tarefa.heap_memory, tarefa.total_pages, tarefa.code_pages, tarefa.heap_pages, tarefa.stack_pages)
        self.tabela_memoria.insert("", tk.END, values=valores)

    def inserir_tarefa_global(self, tarefa):
        valores = (tarefa.total_ram, tarefa.free_ram, tarefa.ram_usage_percentage, tarefa.total_swap, tarefa.free_swap, tarefa.swap_usage_percentage)
        self.tabela_global.insert("", tk.END, values=valores)

    def atualizar_tarefas_processos(self):
        self.carregar_tarefas_processos()
        
    def atualizar_tarefas_memoria(self):
        self.carregar_tarefas_memoria()  
    
    def atualizar_tarefas_global(self):
        self.carregar_tarefas_global()  

    def atualizar_tarefas_automaticamente(self):
        while True:
            self.atualizar_tarefas_processos()
            self.atualizar_tarefas_memoria()
            self.atualizar_tarefas_global()
            time.sleep(3)

if __name__ == "__main__":
    app = GerenciadorTarefas()