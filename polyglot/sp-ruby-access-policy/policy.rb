# frozen_string_literal: true
require 'json'
class Policy
 Rule = Struct.new(:role,:resource,:action,:predicate,keyword_init:true)
 def initialize; @rules=[]; end
 def allow(role:,resource:,action:,&block)
  @rules << Rule.new(role:role,resource:resource,action:action,predicate:block || ->(_){true})
 end
 def decide(subject:,resource:,action:,context:{})
  matching=@rules.select{|r|r.role==subject.fetch(:role) && r.resource==resource && r.action==action}
  # explicit default deny, never grant if attributes fail or any rule is missing.
  granted=matching.any?{|r|r.predicate.call(context.merge(subject:subject))}
  {'decision'=>granted ? 'ALLOW':'DENY','subject'=>subject.fetch(:id),'resource'=>resource,'action'=>action,'rules_evaluated'=>matching.size}
 end
end
if $PROGRAM_NAME==__FILE__
 p=Policy.new;p.allow(role:'analyst',resource:'reports',action:'read') {|c| c[:subject][:mfa] && c[:region]=='apac'}
 puts JSON.pretty_generate(p.decide(subject:{id:'user42',role:'analyst',mfa:true},resource:'reports',action:'read',context:{region:'apac'}))
end
