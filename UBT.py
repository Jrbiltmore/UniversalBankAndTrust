import os
import uuid

project_structure = {
    'blockchain': ['__init__.py', 'chain.py', 'block.py', 'transaction.py', 'quantum_security.py', 'consensus.py', 'smart_contracts.py'],
    'mining': ['__init__.py', 'shors_algorithm.py', 'mining_manager.py', 'quantum_miner.py'],
    'quantum': {
        '__init__.py': None,
        'quantum_algorithms.py': None,
        'quantum_interface.py': None,
        'error_correction': ['__init__.py', 'qec.py', 'error_mitigation.py']
    },
    'wallet_app/lib': {
        '__init__.py': None,
        'models': ['wallet_model.dart', 'transaction_model.dart'],
        'views': ['wallet_view.dart', 'transaction_view.dart', 'settings_view.dart'],
        'controllers': ['wallet_controller.dart', 'transaction_controller.dart'],
        'smart_contract_interface.dart': None,
        'quantum_wallet_functions.dart': None
    },
    'api': ['__init__.py', 'blockchain_operations.py', 'quantum_computing_access.py', 'external_integration.py'],
    'utils': ['docker_setup.sh', 'ci_cd_pipeline.yml', 'quantum_simulation_tools.py', 'network_monitoring.py'],
    'tests': ['blockchain_tests.py', 'mining_tests.py', 'quantum_tests.py', 'consensus_tests.py', 'smart_contract_tests.py', 'api_tests.py'],
    'docs': ['README.md', 'DEVELOPER_GUIDE.md', 'API_REFERENCE.md', 'SECURITY.md', 'QUANTUM_INTEGRATION.md'],
    'UniversalBankAndTrust': ['__init__.py', 'bank_operations.py', 'trust_services.py']
}

def create_file(path):
    """Creates a file at the specified path with a UUID commented at the top."""
    file_uuid = str(uuid.uuid4())
    with open(path, 'w') as f:
        if path.endswith('.py'):
            f.write(f"# UUID: {file_uuid}\n\n")
        elif path.endswith('.dart'):
            f.write(f"// UUID: {file_uuid}\n\n")
        elif path.endswith('.sh') or path.endswith('.yml') or path.endswith('.md'):
            f.write(f"# UUID: {file_uuid}\n\n")

def create_project_structure(base_path, structure):
    """Recursively creates the project directory structure and files."""
    for key, value in structure.items():
        current_path = os.path.join(base_path, key)
        if isinstance(value, dict):  # It's a directory with nested structure
            os.makedirs(current_path, exist_ok=True)
            create_project_structure(current_path, value)
        elif isinstance(value, list):  # It's a list of files in the current directory
            os.makedirs(current_path, exist_ok=True)
            for file_name in value:
                file_path = os.path.join(current_path, file_name)
                create_file(file_path)
        elif value is None:  # Single file in the directory
            create_file(current_path)

# Create the project structure in the current directory (.)
create_project_structure('.', project_structure)

print("Project structure with UniversalBankAndTrust and UUIDs created successfully.")
