import sys


def helloWorld(args, params):
    to = 'World'
    if params['variables']['to'] != '':
        to = params['variables']['to']
    text = 'Hello, {}'.format(to)
    if params['toggle']['excited']:
        text += '!'
    print(text)


commands = {
    'hello': {
        'function': helloWorld,
        'comment': 'Hello world command',
        'variables': {
            'to': {
                'arg_offset': 0,
                'name': 'To',
                'comment': 'Specify whom you\'re saying your helloes to'
            },
        },
        'toggle': {
            'excited': {
                'call': ['-e', '--excited'],
                'comment': 'When selected adds exclamation point to the end'
            }
        }
    },
}


def wrongUsage(args):
    print(f'Error: Command missused, try {args[0]} [command] -h',
          f'or {args[0]} [command] --help')
    exit()


def fetchSyntax(placeholder_name, prop_dict):
    tmp_name, tmp_req, tmp_comment = [placeholder_name, ['[ ', ' ]'], '']
    if 'name' in prop_dict:
        tmp_name = prop_dict['name']
    elif 'call' in prop_dict:
        tmp_name = " | ".join(prop_dict["call"])
    if 'required' in prop_dict and prop_dict['required']:
        tmp_req = ['', '']
    if 'comment' in prop_dict:
        tmp_comment = prop_dict['comment']
    return [tmp_name, tmp_req, tmp_comment]


def helpParse(com, args):
    helper = com
    if args[1] not in ['-h' '--help'] and args[1] in com.keys():
        helper = {args[1]: com[args[1]]}
    else:
        print(f'''For more details about command use: \
{args[0]} <command> --help''')
    for x, y in helper.items():
        tmp_comment, prp_m = ['', {'variables': 'Values', 'toggle': 'Options'}]
        if 'comment' in y:
            tmp_comment = y['comment']
        props = {a: y[z] for z, a in prp_m.items() if z in y}
        if args[1] in com.keys():
            for gen in ['Values', 'Options']:
                if gen not in props:
                    props[gen] = {}
            order = {str(a['arg_offset']): z
                     for z, a in props['Values'].items() if 'arg_offset' in a}
            order_keys, ordered, com_args = [list(order.keys()), [], args[1]]
            for order_suposed_index in range(len(order_keys)):
                if order_suposed_index != int(order_keys[order_suposed_index]):
                    raise IndexError(
                        'Missing index, check your command dictionary')
                ordered.append(
                    props['Values'][order[order_keys[order_suposed_index]]])
            ordered.extend([y['toggle'][com_tg]
                            for com_tg in props['Options'].keys()])
            for com_data in ordered:
                call, optional, _ = fetchSyntax('', com_data)
                com_args += ' {}{}{}'.format(optional[0], call, optional[1])
            print(f'Command reference: {args[0]} {com_args}')
        print('\n{:<4}{:<32}{}'.format('', x, tmp_comment))
        for z, a in props.items():
            print('{:<8}{:<40}'.format('', z + ':'))
            for b, c in a.items():
                tmp_name, tmp_req, tmp_cmn = fetchSyntax(b, c)
                print('{:<14}{:<26}{}'
                      .format('', tmp_req[0] + tmp_name + tmp_req[1], tmp_cmn))


if any(r in sys.argv for r in ['--help', '-h']):
    helpParse(commands, sys.argv)
elif len(sys.argv) > 1 and sys.argv[1] in commands.keys():
    params = {}
    if 'toggle' in commands[sys.argv[1]].keys() \
            and len(commands[sys.argv[1]]['toggle'].keys()) > 0:
        params['toggle'] = {}
        calls = {x: commands[sys.argv[1]]['toggle'][x]['call']
                 for x in commands[sys.argv[1]]['toggle']}
        for x in calls.keys():
            params['toggle'][x] = any(y in sys.argv for y in calls[x])
    if 'variables' in commands[sys.argv[1]].keys() \
            and len(commands[sys.argv[1]]['variables'].keys()) > 0:
        params['variables'], mixed_values = [{}, []]
        variables = [x for x in commands[sys.argv[1]]['variables'].keys()]
        for variable in variables:
            var, val = [commands[sys.argv[1]]['variables'][variable], '']
            if 'arg_offset' in var.keys() \
                    and len(sys.argv) > (2 + var['arg_offset']):
                arg_set, tgl_d = [2 + var['arg_offset'],
                                  commands[sys.argv[1]]['toggle'].items()]
                toggle_calls = [toggler for _, com_data in tgl_d
                                for toggler in com_data['call']]
                if sys.argv[arg_set] not in toggle_calls:
                    val = sys.argv[2 + var['arg_offset']]
            if 'call' in var.keys() and type(var['call']) == list:
                pre_val = [arg for call in var['call']
                           for arg in sys.argv if call in arg]
                if len(pre_val) > 0:
                    val = (pre_val[0].split('='))[1]
            if 'required' in var and var['required'] and val == '':
                wrongUsage(sys.argv)
            else:
                params['variables'][variable] = val
    commands[sys.argv[1]]['function'](sys.argv, params)
else:
    wrongUsage(sys.argv)
exit()
