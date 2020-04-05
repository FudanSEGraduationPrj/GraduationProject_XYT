from os import listdir
from os.path import join
import json
import copy
import spacy


class AspectMatcher(object):
    """
    A class used to match aspects expressed in the sentences
    """
    def __init__(self, vocabulary_path='vocabulary.txt', rule_dir='rules'):
        self.vocabulary = self.construct_vocabulary(vocabulary_path)
        self.libs = set([line.strip() for line in open('final_tags.txt').readlines()])
        self.rule_list = self.load_rules(rule_dir)
        self.nlp = spacy.load('en_core_web_sm')

    def construct_vocabulary(self, vocabulary_path):
        """
        This method constructs vocabularies from the given file
        :param vocabulary_path: the path to the vocabulary file
        :return vocabulary: the vocabulary in the format of a dictionary
        """
        vocabulary = {}
        voc_file = open(vocabulary_path)
        for line in voc_file.readlines():
            text = line.strip()
            index = text.index(':')
            words = str(text[index + 2:-1]).split('|')
            vocabulary[str(text[:index])] = set(words)
        return vocabulary

    def load_rules(self, rule_dir):
        """
        This method loads rules in the rule directory.
        :param rule_dir: path of directory where the rules are stored
        :return rule_list: rule list
        """
        rule_list = {}
        for rule_file in listdir(rule_dir):
            if rule_file.endswith('.json'):
                #aspect为community,compatibility等
                aspect = rule_file[:-5]
                rule_list[aspect] = []
                for rule_line in open(join(rule_dir, rule_file)).readlines():
                    rule_json = json.loads(rule_line.strip())
                    rule_json['aspect'] = aspect
                    #rule_list[community]=
                    #rule_list[compatibility]=
                    rule_list[aspect].append(rule_json)
        return rule_list

    def neg_sentiment(self, sentiment):
        """
        Negate the sentiment
        :param sentiment: sentiment of the sentence
        :return sentiment: negated sentiment
        """
        if sentiment == 'POS':
            return 'NEG'
        elif sentiment == 'NEG':
            return 'POS'
        else:
            return 'NEU'

    def satisfy_restriction(self, doc, match_dict, restriction):
        """
        Check if the sentence meets the dependency restrictions of the rule.
        :param doc: sentence parsed by spacy
        :param match_dict: a dictionary which records the positions of matched tokens by the rule
                           (without covnsidering dependency restrictions)
        :param restriction: restriction relation between units in the rules
        :return: positions of tokens which meet the restrictions
        """
        #restriction[0]为rule_unit序号
        #match_dict[rule_unit_ind]:符合某个rule_unit的所有word_ind
        word_list = match_dict[restriction[0]]

        # restriction[1]为restriction[0]对应的rule_unit的dependency的rule_unit序号
        target_list = match_dict[restriction[1]]
        #word_ind和target_ind为词序号
        for word_ind in word_list:
            for target_ind in target_list:
                if (int(target_ind) > int(word_ind) and int(restriction[1]) > int(restriction[0])) or (
                        int(target_ind) < int(word_ind) and int(restriction[1]) < int(restriction[0])):
                    word = doc[word_ind]
                    target = doc[target_ind]
                    target_pos = doc[target_ind].pos_
                    while word.head != word:
                        word = word.head
                        if word.pos_ == target_pos:
                            if word == target:
                                return {'word_ind': word_ind, 'target_ind': target_ind}
                            else:
                                break
        return False

    def find_neg(self, doc):
        """
        This method detects the negated parts of the given sentence
        :param doc: sentence parsed by spacy
        :return neg_parts: a list of negated parts (represented with starting position and ending position)
        """
        def recursive_tree(node, node_list=None):
            if node_list is None:
                node_list = []
            if node.n_lefts + node.n_rights > 0:
                node_list += [child.i for child in node.children if child.dep_ != 'conj']
                [recursive_tree(child, node_list) for child in node.children if child.dep_ != 'conj']
            return node_list
        neg_parts = []
        for ind in range(0, len(doc)):
            if doc[ind].dep_ == 'neg':
                word = doc[ind]
                node_list = [word.head.i]
                node_list = recursive_tree(word.head, node_list)
                neg_parts.append((min(node_list), max(node_list)))
        return neg_parts

    def match_rule(self, doc, rule_dict):
        """
        This method extracts aspect from the given sentence
        :param doc: sentence parsed by spacy
        :param rule_dict: rules extracted in dict format
        :return aspect: aspect found in the text
        """
        #doc is text
        #rule_dict = {"rules": [{"ADJ_COM_POS": "", "dep": "1"}, {"NOUN_COM": "", "POS": "NOUN"}], "default_sentiment": "POS"}
        rule_units = copy.deepcopy(rule_dict['rules'])#rule unit
        match_dict = {}
        min_offset = 0
        restrictions = []
        doc_len = len(doc)

        # find all matched vocabularies
        for ind in range(0, len(rule_units)):
            match_dict[str(ind)] = []
            set_min_offset = 0
            if 'dep' in rule_units[ind]:
                dep = rule_units[ind]['dep']
                rule_units[ind].pop('dep')
                restrictions.append((str(ind), dep))
            if 'POS' in rule_units[ind]:
                rule_units[ind].pop('POS')
            #对某一条规则的某个rule_unit而言，去除掉dep和pos后的主体
            key, value = rule_units[ind].popitem()

            #对某一条规则的某个rule_unit而言
            for i in range(min_offset, doc_len):#对每个词而言
                if value == 'lib':
                    #doc:英文分词doc[0]表示第一个词
                    if (doc[i].text.lower() == 'it') or (doc[i].pos_ == 'PROPN') or (doc[i].text.lower() in self.libs):
                        #某个匹配上的rule_unit对应的词下标，某个rule_unit可能找到多个匹配的词
                        match_dict[str(ind)].append(i)
                        #匹配上某个rule_unit之后，对同一个rule_unit而言，剩下的文本接着匹配，每次某个rule_unit第一次匹配上一个词就将min_offset设为下一个词坐标
                        if set_min_offset == 0:
                            min_offset = i+1
                            set_min_offset = 1
                #{"VERB|NOUN": "pos", "dep": "1"}，不针对某个方面而言的通用词性
                elif value == 'pos':
                    keys = key.split('|')
                    if doc[i].pos_ in keys:
                        # 某个匹配上的rule_unit对应的词下标
                        match_dict[str(ind)].append(i)
                        if set_min_offset == 0:
                            min_offset = i+1
                            set_min_offset = 1

                #针对每个方面而言的特殊词语（不一定）
                else:
                    voc = set([])
                    for voc_key in key.split('|'):
                        #从vocabulary中取得具体词语进行匹配
                        voc = voc.union(self.vocabulary[voc_key])
                    #reliability.json:ERROR_NAME
                    #匹配ERROR_NAME的时候找到了error词语
                    #单个词匹配
                    if (doc[i].lemma_.lower() in voc) or (key == 'ERROR_NAME' and 'error' in doc[i].lemma_.lower()):
                        match_dict[str(ind)].append(i)
                        if set_min_offset == 0:
                            min_offset = i+1
                            set_min_offset = 1
                    #单个词未匹配上考虑多个词匹配
                    else:
                        #并非最后一个词
                        if (i+1) < doc_len:
                            #两个词连起来匹配，如come with
                            phrase = doc[i].lemma_.lower() + ' ' + doc[i+1].lemma_.lower()
                            if phrase in voc:
                                match_dict[str(ind)].append(i)
                                if set_min_offset == 0:
                                    min_offset = i+2
                                    set_min_offset = 1
                            #三个词连起来匹配，如have a look
                            elif (i+2) < doc_len:
                                phrase = ' '.join([doc[inner_i].lemma_.lower() for inner_i in range(i, i+3)])
                                # print('phrase > 2 ', phrase, voc)
                                if phrase in voc:
                                    match_dict[str(ind)].append(i)
                                    if set_min_offset == 0:
                                        min_offset = i+3
                                        set_min_offset = 1
            #某条规则的某个rule_unit未找到匹配词，则该规则不匹配
            if len(match_dict[str(ind)]) == 0:
                return None

        restricted_dict = {}
        #restrictions:[(0,1),(1,2)]
        for restriction in restrictions:
            restriction_result = self.satisfy_restriction(doc, match_dict, restriction)
            if restriction_result is False:
                return None
            else:
                #restrictioin = (1,2),1为rule_unit序号，2为dependency对应的rule_unit序号
                restricted_dict[str(restriction[0])] = restriction_result['word_ind']
                restricted_dict[str(restriction[1])] = restriction_result['target_ind']
        start_pos = restricted_dict[str(0)]
        end_pos = restricted_dict[str(len(rule_units)-1)]

        neg_parts = self.find_neg(doc)
        if len(neg_parts) > 0:
            for neg_part in neg_parts:
                if neg_part[1] >= end_pos and neg_part[0] <= start_pos:# neg_part['start'] <= matched_start and neg_part['end'] >= matched_end:
                    return {'aspect': rule_dict['aspect'],
                            'sentiment': self.neg_sentiment(rule_dict['default_sentiment']),
                            'negated': True, 'rule': rule_dict['rules']}
        return {'aspect': rule_dict['aspect'], 'sentiment': rule_dict['default_sentiment'],
                'negated': False, 'rule': rule_dict['rules']}

    def identify_aspect(self, text):
        """
        identify the aspect from the sentence
        :param text: string of the sentence
        :return detected_aspect: identified aspect
        """
        aspects = ['community', 'compatibility', 'performance', 'reliability', 'usability', 'documentation', 'functional']
        detected_aspect = {'sentiment': '', 'aspect': ''}
        #倒数第一个字符是问号，即为问句，问句无情感倾向
        if text[-1] == '?':
            return detected_aspect
        doc = self.nlp(text)
        for aspect in aspects:
            if (detected_aspect['sentiment'] == '') or (aspect not in ['functional']):
                #对某个方面的某条规则而言，aspect=community,functional等
                for rule in self.rule_list[aspect]:
                    #查看某条文本是否符合某条规则，得到匹配结果
                    match_result = self.match_rule(doc, rule)
                    if match_result:
                        #sentiment为多个方面对应的情感极性字符串
                        detected_aspect['sentiment']+=(match_result['sentiment'] + ' ')
                        #aspect为多个方面字符串
                        detected_aspect['aspect']+=(match_result['aspect'] + ' ')
                        break
        #原字符串包含或者情感检测出compatibility方面
        if 'compatibility' in text.lower() or 'compatibility' in detected_aspect['aspect']:
            if 'reliability' in detected_aspect['aspect']:
                aspect_list = detected_aspect['aspect'].strip().split(' ')
                senti_list = detected_aspect['sentiment'].strip().split(' ')
                print(aspect_list, senti_list)
                # 文本中检测出compatibility方面且检测出reliability方面
                if 'compatibility' in aspect_list:
                    rel_ind = aspect_list.index('reliability')
                    aspect_list.pop(rel_ind)
                    senti_list.pop(rel_ind)
                    #除去reliability方面
                    detected_aspect['aspect'] = ' '.join(aspect_list)
                    detected_aspect['sentiment'] = ' '.join(senti_list)

                #文本中含有compatibility字符串但没有检测出compatibility方面且检测出reliability方面
                else:

                    detected_aspect['aspect'] = detected_aspect['aspect'].replace('reliability', 'compatibility')
        if 'performance' in text.lower() or 'speed' in text.lower():
            if 'reliability' in detected_aspect['aspect']:
                aspect_list = detected_aspect['aspect'].strip().split(' ')
                senti_list = detected_aspect['sentiment'].strip().split(' ')
                if 'performance' in detected_aspect['aspect']:
                    rel_ind = aspect_list.index('reliability')
                    aspect_list.pop(rel_ind)
                    senti_list.pop(rel_ind)
                    detected_aspect['aspect'] = ' '.join(aspect_list)
                    detected_aspect['sentiment'] = ' '.join(senti_list)
                else:
                    detected_aspect['aspect'] = detected_aspect['aspect'].replace('reliability', 'performance')
        detected_aspect['aspect'] = detected_aspect['aspect'].strip()
        return detected_aspect
