from handtype.hand import Hand
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Player:
    VERSION = "Inky 0.2"

    def isOneVsOne(self):
        active = 0
        names = []
        for p in self.game_state['players']:
            if p['status'] == 'active':
                active += 1
                names.append(p['name'])
        if active == 2:
            return True, names
        return False, []

    def power(self, hand):
        pass

    def pre_flop_power1(self, hand):
        if hand.rank == 1 and hand.value >= 10:
            return True
        if hand.rank == 0 and hand.value >= 14 and hand.value2 >= 10:
            return True
        return False

    def pre_flop_power3(self, hand):
        if hand.rank == 0 and hand.value <= 7:
            return True
        return False

    def betRequest(self, game_state):
        if not 'in_action' in game_state.keys():
            return 0

        for p in game_state['players']:
            print("QQQ, %d, %s, %s" % (game_state['round'], p['name'], p['status']))

        self.game_state = game_state
        me = game_state['players'][game_state['in_action']]
        call = game_state['current_buy_in'] - me['bet']
        my_cards = me['hole_cards']
        community_cards = game_state['community_cards']
        pot = game_state['pot']
        blind = game_state['small_blind'] * 2
        bet_index = game_state['bet_index']
        rais = game_state['minimum_raise']

        isOneVsOne, names = self.isOneVsOne()
        if isOneVsOne and 'PythonPokerTeam' in names:
            names.remove('PythonPokerTeam')
            enemy_name = names[0]
            print 'enemy_name=%s' % enemy_name
            enemy_player = None
            for player in game_state['players']:
                if player['name'] == enemy_player:
                    enemy_player = player
                    if enemy_name == 'Awesome Incredible Poker Bot':
                        return call + rais
                    if enemy_name == 'LeanNodeJS':
                        if enemy_player['stack'] <= 2*rais:
                            return call + enemy_player['stack']
                        return call + rais

        if len(community_cards) == 0:
            print 'cards_str:'
            cards_str = []
            for c in my_cards:
                cards_str.append(str(c))
            print cards_str
            # pre flop

            hand = Hand(my_cards)
            print "HAND %s" % hand
            if self.pre_flop_power1(hand):
                print 'power'
                if call >= blind*3:
                    return call
                else:
                    return call + rais
            if self.pre_flop_power3(hand):
                print 'pass'
                return 0
            print 'middle'

            if call <= blind * 3 and bet_index < 1:
                return call
            if bet_index >= 1 and 3 * me['bet'] <= call:
                return 0
            else:
                return call

            return 0

        else:
            print 'board_str:'
            cards = my_cards + community_cards
            board_str = []
            for c in community_cards:
                board_str.append(str(c))
            print board_str
            hand = Hand(cards)
            print "HAND %s" % hand
            if hand.rank >= 2:
                return call + 2 * rais

            if hand.rank == 1 and hand.value >= 10:
                return call + rais

            if hand.rank == 0 and hand.value == 14:
                return call

            if hand.rank == 0 and hand.value < 6:
                return 0
        return call

    def showdown(self, game_state):
        pass
