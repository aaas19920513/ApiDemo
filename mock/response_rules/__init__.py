from .providers import ResponseRuleProvider
from .rule_matchers import (RequestParamExistsMatcher, RequestParamContainsValueMatcher,
                                                   RequestParamNotContainsValueMatcher)

response_rules_provider = ResponseRuleProvider()
response_rules_provider.register_matcher_class(RequestParamExistsMatcher)
response_rules_provider.register_matcher_class(RequestParamContainsValueMatcher)
response_rules_provider.register_matcher_class(RequestParamNotContainsValueMatcher)
