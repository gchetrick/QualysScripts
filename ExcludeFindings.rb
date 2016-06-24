#!/usr/bin/env ruby
require 'nokogiri'
require 'open-uri'
require 'optparse'

options = {}

optparse = OptionParser.new do |opts|
  opts.banner = "Usage: ExcludeFindings.rb [options]"

  options[:ip] = nil
  opts.on( '-i', '--ip [ip]', 'IP to view') do |ip|
    options[:ip] = ip
  end

  options[:qid] = nil
  opts.on( '-q', '--qid [qid]', 'QID to search on') do |qid|
    options[:qid] = qid 
  end

  options[:comment] = ""
  opts.on( '-c', '--comment [comment]', 'Comments for the ticket') do |comment|
    options[:comment] = comment
  end  

  opts.on( '-h', '--help', 'Display this screen') do
    puts opts
    exit
  end
end

optparse.parse!

#puts "IP ADDR #{options[:ip]}" if options[:ip]
#puts "QID #{options[:qid]}" if options[:qid]

uri = "https://qualysapi.qualys.com/msp/ignore_vuln.php?action=ignore&qids=#{options[:qid]}&ips=#{options[:ip]}&comments=#{options[:comment]}"

#puts uri

#Uncomment this line and comment the one below if proxy auth is necessary
#results = Nokogiri::XML(open(uri, :http_basic_authentication=>["USERNAME", "PASSWORD"], :proxy_http_basic_authentication=>["http://<PROXY_IP:8080>,"USERNAME", "PASSWORD"]))
results = Nokogiri::XML(open(uri))
#puts results
results.xpath("//RETURN").each do |status|
  if status['status'] == "FAILED"
    puts "#{status['status']} : #{results.xpath("//MESSAGE").text} -- ITEM: #{options[:qid]} - #{options[:ip]}"
  else
    puts "#{status['status']} -- #{options[:qid]}:#{options[:ip]}"
  end
end
