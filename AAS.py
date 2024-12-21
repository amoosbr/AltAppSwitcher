import os
import shutil

def MakeStaticStr():
    fsrc = open("./Assets/AltAppSwitcherConfig.txt", "r")
    if not os.path.exists("./Sources/Config/_Generated"):
        os.makedirs("./Sources/Config/_Generated")
    fdst = open("./Sources/Config/_Generated/ConfigStr.h", "w")
    fdst.write("static const char ConfigStr[] =\n" )
    for line in fsrc:
        fdst.write("\"")
        fdst.write(line.strip("\n").replace('"', r'\"'))
        fdst.write(r"\n")
        fdst.write("\"")
        fdst.write("\n")
    fdst.write(";")

def MakeDirIfNeeded(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def Clean():
    if os.path.exists("./Output"):
        shutil.rmtree("./Output");

def CopyDirStructure(src, dst):
    for x in os.listdir(src):
        px = os.path.join(src, x)
        if not os.path.isdir(px):
            continue
        dstpx = os.path.join(dst, x)
        MakeDirIfNeeded(dstpx)
        CopyDirStructure(px, dstpx)

def MakeDirs(conf, arch):
    MakeDirIfNeeded("./Output")
    MakeDirIfNeeded(f"./Output/{conf}_{arch}")
    MakeDirIfNeeded(f"./Output/{conf}_{arch}/Objects")
    MakeDirIfNeeded(f"./Output/{conf}_{arch}/AAS")
    MakeDirIfNeeded(f"./Output/{conf}_{arch}/Updater")
    CopyDirStructure("./Sources", f"./Output/{conf}_{arch}/Objects")

def Copy(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copy(src, dst)

def MakeCompileCommands(file, args):
    outf = open(file, 'w')
    outf.write("[\n")
    for fname in args:
        inf = open(fname, 'r')
        content = inf.read()
        # if last element removes ",\n"
        if fname == args[-1]:
            outf.write(content[0:-2])
        else:
            outf.write(content)
    outf.write("\n]")
    outf.close()

def EmbedAndDeleteManifest(exePath):
    if not os.path.exists(f"{exePath}.manifest"):
        return
    os.system(f"mt.exe -manifest \"{exePath}.manifest\" -outputresource:\"{exePath}\"")
    os.remove(f"{exePath}.manifest")

def deploy(arch):
    srcDir = f"./Output/Release_{arch}"
    if os.path.exists(srcDir):
        shutil.rmtree(srcDir)
    dstDir = "./Output/Deploy"
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    tempDir = f"./Output/Deploy/Temp_{arch}"
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)

    os.system(f"mingw32-make ARCH={arch} CONF=Release")

    shutil.copytree(srcDir, tempDir)
    shutil.rmtree(f"{tempDir}/Objects");
    EmbedAndDeleteManifest(f"{tempDir}/AltAppSwitcher.exe")
    EmbedAndDeleteManifest(f"{tempDir}/Updater.exe")
    EmbedAndDeleteManifest(f"{tempDir}/Settings.exe")

    zipFile = f"{dstDir}/AltAppSwitcher_{arch}"
    shutil.make_archive(zipFile, "zip", tempDir)

def MakeArchive(srcDir, dstZip):
    tempDir = f"{dstZip}" 
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)
    shutil.copytree(srcDir, tempDir)
    for x in os.listdir(tempDir):
        if x.endswith(".exe"):
            EmbedAndDeleteManifest(os.path.join(tempDir, x))
    shutil.make_archive(dstZip, "zip", tempDir)

import sys
if __name__ == "__main__": 
    args = sys.argv[1:]
    fn = args[0]
    if fn == "Copy":
        Copy(args[1], args[2])
    elif fn == "MakeDirs":
        MakeDirs(args[1], args[2])
    elif fn == "Clean":
        Clean()
    elif fn == "MakeCompileCommands":
        MakeCompileCommands(args[1], args[2:])
    elif fn == "MakeArchive":
        MakeArchive(args[1], args[2])
