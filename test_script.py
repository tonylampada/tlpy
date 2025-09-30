#!/usr/bin/env python3
"""
Script de teste para demonstrar funcionalidade do container
"""

def main():
    print("🐍 Python DevContainer - Teste de Funcionalidade\n")

    # Testar imports básicos
    try:
        import sys
        print(f"✅ Python {sys.version.split()[0]} funcionando")
    except ImportError as e:
        print(f"❌ Erro: {e}")

    # Testar ferramentas instaladas
    tools = {
        "rich": "Terminal com formatação rica",
        "pytest": "Framework de testes",
        "black": "Formatter de código",
        "mypy": "Type checker",
        "jupyter": "Notebooks interativos"
    }

    print("\n📦 Pacotes pré-instalados:")
    for package, description in tools.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<10} - {description}")
        except ImportError:
            print(f"  ❌ {package:<10} - Não encontrado")

    # Demonstração com Rich
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()

        table = Table(title="\n🚀 Recursos do Container")
        table.add_column("Categoria", style="cyan", no_wrap=True)
        table.add_column("Ferramenta", style="magenta")
        table.add_column("Status", style="green")

        table.add_row("Python", "uv package manager", "✅ Instalado")
        table.add_row("Python", "Jupyter notebooks", "✅ Instalado")
        table.add_row("JavaScript", "Node.js LTS", "✅ Instalado")
        table.add_row("JavaScript", "pnpm", "✅ Instalado")
        table.add_row("Sistema", "ripgrep (rg)", "✅ Instalado")
        table.add_row("Sistema", "eza (modern ls)", "✅ Instalado")

        console.print(table)

    except ImportError:
        print("\n💡 Para ver uma demonstração completa, instale o rich:")
        print("   sudo uv pip install --system rich")

if __name__ == "__main__":
    main()