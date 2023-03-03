import subprocess
import json 
from time import sleep
import sys
import os
import json

#TODO must create cleos import script

class Genesis:

    #initializing Genesis object
    def __init__(self) -> None:

        with open(f'contract_paths.json', 'r') as data:
                contract_paths = json.load(data)

        self.private_key       = ''
        self.public_key        = ''
        self.node_folder       = 'genesis.node'
        self.system_currency   = 'eos'
        
        #contract paths
        self.eosio_boot_path   = contract_paths['paths_to_contracts']['eosio.boot']
        self.eosio_system_path = contract_paths['paths_to_contracts']['eosio.system']
        self.eosio_token_path  = contract_paths['paths_to_contracts']['eosio.token']

        os.mkdir(f'./{self.node_folder}')

        #features to activate
        self.features          = ["825ee6288fb1373eab1b5187ec2f04f6eacb39cb3a97f356a07c91622dd61d16",
                                  "c3a6138c5061cf291310887c0b5c71fcaffeab90d5deb50d3b9e687cead45071",
                                  "bf61537fd21c61a60e542a5d66c3f6a78da0589336868307f94a82bccea84e88",
                                  "5443fcf88330c586bc0e5f3dee10e7f63c76c00249c87fe4fbf7f38c082006b4",
                                  "f0af56d2c5a48d60a4a5b5c903edfb7db3a736a94ed589d0b797df33ff9d3e1d",
                                  "2652f5f96006294109b3dd0bbde63693f55324af452b799ee137a81a905eed25",
                                  "8ba52fe7a3956c5cd3a656a3174b931d3bb2abb45578befc59f283ecd816a405",
                                  "ad9e3d8f650687709fd68f4b90b41f7d825a365b02c23a636cef88ac2ac00c43",
                                  "68dcaa34c0517d19666e6b33add67351d8c5f69e999ca1e37931bc410a297428",
                                  "e0fb64b1085cc5538970158d05a009c24e276fb94e1a0bf6a528b48fbc4ff526",
                                  "ef43112c6543b88db2283a2e077278c315ae2c84719a8b25f25cc88565fbea99",
                                  "4a90c00d55454dc5b059055ca213579c6ea856967712a56017487886a4d4cc0f",
                                  "1a99a59d87e06e09ec5b028a9cbb7749b4a5ad8819004365d02dc4379a8b7241",
                                  "4e7bf348da00a945489b2a681749eb56f5de00b900014e137ddae39f48f69d67",
                                  "4fca8bd82bbd181e714e283f83e1b45d95ca5af40fb89ad3977b653c448f78c2",
                                  "299dcb6af692324b899b39f16d5a530a33062804e41f09dc97e9f156b4476707"]
        
        #system contracts to create
        #important do not change
        self.system_accounts   = ['eosio.bpay',
                                  'eosio.msig',
                                  'eosio.names',
                                  'eosio.ram',
                                  'eosio.ramfee',
                                  'eosio.saving',
                                  'eosio.stake',
                                  'eosio.token',
                                  'eosio.vpay',
                                  'eosio.wrap',
                                  'eosio.rex',
                                  'eosio.reserv']

    #creating eosio wallet and importing keys
    def create_wallet(self):

        try:

            print('Creating eosio wallet. . .')

            wallet_data   = subprocess.Popen(["cleos", "wallet", "create", "--file", f"./{self.node_folder}/walletPassword.txt"]).communicate()[0]
            dev_keys_data = subprocess.Popen(["cleos", "create", "key", "--file", f"./{self.node_folder}/devKeys.txt"]).communicate()[0]

            with open(f'./{self.node_folder}/devKeys.txt', 'r') as file:
                data = file.read()
                self.private_key = data.strip().split('\n')[0].split(':')[1].strip()
                self.public_key = data.strip().split('\n')[1].split(':')[1].strip()
            
            print('')
            print('Importing dev key. . .')

            import_wallet_data = subprocess.Popen(["cleos", "wallet", "import", "--private-key", f"{self.private_key}"]).communicate()[0]

            print('')
            print(f'[+] Files saved in [./{self.node_folder}/walletPassword.txt] and [./{self.node_folder}/devKeys.txt]')
            print('')
            print('Wallet created successfully!')

        except Exception as error:

            print('An error has occured while creating a wallet!')
            print(error)
        
    #creating scripts
    #starting chain with dedicated .sh(bash) script
    def start_chain(self) -> None:
        try:
            
            print('')
            print('Generating files. . .')

            #generating .sh script
            with open(f'./{self.node_folder}/genesis_start.sh', 'w') as genesis_start:
                genesis_start.write('#!/bin/bash\n')
                genesis_start.write('DATADIR="blockchain/"\n')
                genesis_start.write('\n')
                genesis_start.write('if [ ! -d $DATADIR ]; then\n')
                genesis_start.write('  mkdir -p $DATADIR;\n')
                genesis_start.write('fi\n')
                genesis_start.write('\n')
                genesis_start.write('nodeos \\\n')
                genesis_start.write('--genesis-json $DATADIR"/../genesis.json" \\\n')
                genesis_start.write('--plugin eosio::producer_plugin \\\n ')
                genesis_start.write('--plugin eosio::producer_api_plugin \\\n')
                genesis_start.write('--plugin eosio::chain_plugin \\\n')
                genesis_start.write('--plugin eosio::chain_api_plugin \\\n')
                genesis_start.write('--plugin eosio::http_plugin \\\n')
                genesis_start.write('--plugin eosio::history_api_plugin \\\n')
                genesis_start.write('--plugin eosio::history_plugin \\\n')
                genesis_start.write('--plugin eosio::net_plugin \\\n')
                genesis_start.write('--plugin eosio::net_api_plugin \\\n')
                genesis_start.write('--filter-on=* \\\n')
                genesis_start.write('--data-dir $DATADIR"/data" \\\n')
                genesis_start.write('--blocks-dir $DATADIR"/blocks" \\\n')
                genesis_start.write('--config-dir $DATADIR"/config" \\\n')
                genesis_start.write('--access-control-allow-origin=* \\\n')
                genesis_start.write('--contracts-console \\\n')
                genesis_start.write('--http-validate-host=false \\\n')
                genesis_start.write('--verbose-http-errors \\\n')
                genesis_start.write('--enable-stale-production \\\n')
                genesis_start.write('--p2p-max-nodes-per-host 100 \\\n')
                genesis_start.write('--connection-cleanup-period 10 \\\n')
                genesis_start.write('--producer-name eosio \\\n')
                genesis_start.write('--http-server-address 0.0.0.0:8888 \\\n')
                genesis_start.write('--p2p-listen-endpoint bis.blockchain-servers.world:9010 \\\n')
                genesis_start.write(f'--signature-provider {self.public_key}=KEY:{self.private_key} \\\n')
                genesis_start.write('>> $DATADIR"/nodeos.log" 2>&1 & \\\n')
                genesis_start.write('echo $! > $DATADIR"/eosd.pid"')

            #generating genesis.json file
            data = {
                "initial_timestamp": "2023-01-05T08:55:11.000",
                "initial_key": f"{self.public_key}",
                "initial_configuration": {
                    "max_block_net_usage": 1048576,
                    "target_block_net_usage_pct": 1000,
                    "max_transaction_net_usage": 524288,
                    "base_per_transaction_net_usage": 12,
                    "net_usage_leeway": 500,
                    "context_free_discount_net_usage_num": 20,
                    "context_free_discount_net_usage_den": 100,
                    "max_block_cpu_usage": 100000,
                    "target_block_cpu_usage_pct": 500,
                    "max_transaction_cpu_usage": 50000,
                    "min_transaction_cpu_usage": 100,
                    "max_transaction_lifetime": 3600,
                    "deferred_trx_expiration_window": 600,
                    "max_transaction_delay": 3888000,
                    "max_inline_action_size": 4096,
                    "max_inline_action_depth": 4,
                    "max_authority_depth": 6
                },
                "initial_chain_id": "0000000000000000000000000000000000000000000000000000000000000000"
            }

            with open(f'./{self.node_folder}/genesis.json', 'w') as genesis.json:
                json.dump(data, genesis.json, indent=4)

            print('')
            print('Starting chain. . .')

            os.chdir(f'./{self.node_folder}')
            os.chmod('genesis_start.sh', 777)
            os.system('./genesis_start.sh')
            os.chdir('../')

            print('')
            print(f'[+] Scripts generated => [./{self.node_folder}/genesis_start.sh] and [./{self.node_folder}/genesis.json]')
            print('')
            print('Chain started successfully!')
            sleep(4)
        
        except Exception as error:

            print('An error has occured while starting eosio chain!')
            print(error)

    #method that creates system accounts
    def create_accounts(self) -> None:
        try:
            system_accounts = '[ \n'

            for account in self.system_accounts:
                key_pair    = subprocess.Popen(["cleos", "create", "key", "--to-console"], stdout=subprocess.PIPE)
                output      = key_pair.communicate()[0].decode().strip()
                private_key = output[13:64].strip()
                public_key  = output[77:].strip()

                system_accounts += '{'
                system_accounts += f'"NAME": "{account}",\n "PRIVATE_KEY": "{private_key}",\n "PUBLIC_KEY": "{public_key}"\n'
                system_accounts += '},\n'

                subprocess.run(["cleos", "create", "account", "eosio", f"{account}", f"{public_key}"], stdout=subprocess.PIPE)
                sleep(1)
                subprocess.run(["cleos", "wallet", "import", "--private-key", f"{private_key}"], stdout=subprocess.PIPE)
                sleep(1)

            system_accounts = system_accounts[0:len(system_accounts) - 2]
            system_accounts += '\n]'

            json_data = json.loads(system_accounts)

            with open(f'./{self.node_folder}/system_accounts.json', 'w+') as f:
                json.dump(json_data, f, indent=4)

        except Exception as error:

            print('An error has occured while creating system accounts!')
            print(error)    
        
    
    #setting up eosio contracts and activating eosio Blockchain features
    #creating system accounts
    #NOTE! without features it is impossible to set contracts
    def set_contracts(self):
        try:
            
            print('')
            print('Setting up eosio.boot contract. . . ')
            print('curl')
            os.popen('curl --request POST --url http://127.0.0.1:8888/v1/producer/schedule_protocol_feature_activations -d \'{"protocol_features_to_activate":["0ec7e080177b2c02b278d5088611686b49d739925a92d9bfcacd7fc6b74053bd"]}\'').read()
            sleep(2)
            print('boot')
            setting_boot_data = subprocess.Popen(["cleos", "set", "contract", "eosio", f"{self.eosio_boot_path}"]).communicate()[0]

            sleep(2)
            print('')
            print('Activating features. . . ')

            for feature in self.features:
                feature_data  = subprocess.Popen(["cleos", "push", "action", "eosio", "activate" , f"[\"{feature}\"]", "-p", "eosio"]).communicate()[0]
            
            sleep(2)
            print('')
            print('Creating system accounts. . . ')

            self.create_accounts()

            sleep(2)
            print('')
            print('Setting up eosio.system contract. . . ')

            setting_system_data = subprocess.Popen(["cleos", "set", "contract", "eosio", f"{self.eosio_system_path}"]).communicate()[0]
            
            sleep(2)
            print('')
            print('Setting up eosio.token contract. . . ')

            setting_token_data = subprocess.Popen(["cleos", "set", "contract", "eosio.token", f"{self.eosio_token_path}"]).communicate()[0]

            sleep(2)
            print('')
            print(f'[+] System account data saved => [./{self.node_folder}/system_accounts.json]')
            print('')
            print('Contracts initialization successful!')
        except Exception as error:

            print('An error has occured while initializatig contracts!')
            print(error)
        

    #setting up eosio.system contract 
    #setting up eosio.token contract
    def set_currency(self):
        try:
            
            print('')
            print(f'Creating {self.system_currency} tokens. . . ')

            token_create_data = subprocess.Popen(["cleos", "push", "action", "eosio.token", "create", f"[\"eosio\", \"800000000.0000 {self.system_currency}\"]", "-p", "eosio.token@active"]).communicate()[0]

            print('')
            print(f'Issuing {self.system_currency} tokens. . . ')
            sleep(2)
            token_transfer_data = subprocess.Popen(["cleos", "push", "action", "eosio.token", "issue", f"[\"eosio\", \"450000000.0000 {self.system_currency}\", \"Issuing tokens for eosio account\"]", "-p", "eosio@active" ]).communicate()[0]

            print('')
            print('Initializing chain. . . ')
            sleep(2)
            token_transfer_data = subprocess.Popen(["cleos", "push", "action", "eosio", "init", f"[\"0\", \"4,{self.system_currency}\"]", "-p", "eosio@active"]).communicate()[0]

            print('')
            print('Chain initialized successfully!')
            sleep(2)

        except Exception as error:

            print(f'An error has occured while setting up system currency({self.system_currency})!')
            print(error)
    
    #creating and issuing eos tokens to eosio account
    #initializing chain
    def start(self):

        self.create_wallet()
        self.start_chain()
        self.set_contracts()
        self.set_currency()

        print('')
        print('[+] Genesis set up finished!')
        print('')

if __name__ == '__main__':

    try:
        flags = sys.argv

        if flags[1] == '--genesis':
            genesis = Genesis()
            genesis.start()

        elif flags[1] == '--help':
            print('Example: ')
            print('To run server: ./eosio.py --server or python3 eosio.py --server ')
            print('To run client: ./eosio.py --slave or python3 eosio.py --slave ')

    except:
        print('--run the script with --help flag ')
