# a few flags will make this run a skosh faster:
# jruby -0 -J-Xmn512m -J-Xms2048m -J-Xmx2048m -J-server onion_search.rb

# For details on reading WARC records:
# https://iipc.github.io/warc-specifications/specifications/warc-format/warc-1.0/#file-and-record-model
require 'csv'
require 'fileutils'

# using java for two reasons: Java has native threads
# and Java's gzip reader supports concatenated zips
java_import 'java.io.FileInputStream'
java_import 'java.util.zip.GZIPInputStream'

# let failures in child threads tank the whole process
Thread.abort_on_exception = true
Encoding.default_external = Encoding::ASCII_8BIT 

paths = Dir['bulk/*.gz'].shuffle
groups = paths.each_slice((paths.size/32.0).round)

threads = groups.map do |paths|

  # each group of paths is processed in its own thread
  Thread.new do 
    paths.each_with_index do |path,index|
      if File.exists? "#{path}.csv"
        print "Results already exist for #{path}\n"

      else
        print "#{index+1}/#{paths.size}: Processing #{path} ...\n"

        File.open("#{path}.csv.part", "w") do |file|

          onions = Hash.new {|hash, key| hash[key] = [] }
          gz = GZIPInputStream.new(FileInputStream.new(path)).to_io
            
          until gz.eof?
            header = gz.readline("\r\n\r\n").scrub! '*'
            length = header.match(/Content-Length: (.+)\r\n/).captures.first.to_i

            # read the content and the closing delimiter
            # replace invalid utf-8 sequences with an asterix
            content = gz.read(length + 4).scrub! '*'

            # if there is url, then look for .onions
            if match = header.match(/WARC-Target-URI: (.+)\r\n/)
              url = match.captures.first
              content.scan /(?:[a-z2-7]{16}|[a-z2-7]{56})\.onion/i do |onion| 
                file.print [onion.downcase,url].to_csv
              end
            end
          end
          
          gz.close
        end

        FileUtils.move "#{path}.csv.part", "#{path}.csv"
      end
    end
  end
end

# wait for everyone to finish
threads.map &:join