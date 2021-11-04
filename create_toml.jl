using Tar, Inflate, SHA

filename = ARGS[1]
filepath = joinpath("..", filename)

sha = bytes2hex(open(sha256, filepath))
gittreesha1 = Tar.tree_hash(IOBuffer(inflate_gzip(filepath)))

open("../Artifacts.toml", "w") do io
    write(io, "[ExaData]\n")
    write(io, "git-tree-sha1 = \"$(gittreesha1)\"\n")
    write(io, "lazy = true\n")
    write(io, "    [[ExaData.download]]\n")
    write(io, "    url = \"https://web.cels.anl.gov/~mschanen/$filename\"\n")
    write(io, "    sha256 = \"$sha\"\n")
end;
