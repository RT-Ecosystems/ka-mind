# KA-Mind v2.0 — Main CLI
# Technique: NeuraBrain | Library: KA-Mind
from ka_mind.framework.model import KaModel


def main():
    print('='*60)
    print(' KA-Mind v2.0 — NeuraBrain Technique')
    print(' Type :help for commands')
    print('='*60)

    model = KaModel('KA-Mind', domain='General')

    while True:
        try:
            user_input = input('\nYou: ').strip()
            if not user_input: continue
            if user_input.lower() in ['exit','quit']: break

            if user_input.startswith(':train '):
                path = user_input[7:].strip()
                model.train_file(path)

            elif user_input.startswith(':learn '):
                text = user_input[7:].strip()
                n = model.learn(text)
                print(f'Learned: {n} new atoms')

            elif user_input == ':sleep':
                model.deep_sleep()

            elif user_input == ':stats':
                for k, v in model.stats().items():
                    print(f'  {k}: {v}')

            elif user_input.startswith(':save'):
                path = model.save()
                print(f'Saved: {path}')

            elif user_input == ':help':
                print(':train <file>  — train on file')
                print(':learn <text>  — learn text directly')
                print(':sleep         — deep sleep cycle')
                print(':stats         — show stats')
                print(':save          — save model')
                print('anything else  — ask a question')

            else:
                answer = model.think(user_input)
                print(f'KA-Mind: {answer}')

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
