input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb".chars
chunk_size = 4

index = input.each_cons(chunk_size).find_index do |chunk|
  chunk.size == chunk.uniq.size
end
puts index + chunk_size
