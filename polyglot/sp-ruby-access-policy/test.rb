require 'minitest/autorun'; require_relative 'policy'
class PolicyTest<Minitest::Test
 def setup;@p=Policy.new;@p.allow(role:'engineer',resource:'catalog',action:'edit'){|ctx|ctx[:subject][:mfa] && ctx[:ticket_approved]};end
 def test_default_deny;assert_equal 'DENY',@p.decide(subject:{id:'1',role:'guest',mfa:true},resource:'catalog',action:'edit')['decision'];end
 def test_context_gating;user={id:'1',role:'engineer',mfa:true};assert_equal 'DENY',@p.decide(subject:user,resource:'catalog',action:'edit')['decision'];assert_equal 'ALLOW',@p.decide(subject:user,resource:'catalog',action:'edit',context:{ticket_approved:true})['decision'];end
end
