#! /usr/bin/env python

import enum
from git import Repo
import os
print(" ################################### ");
print(" #  onion environement install    #");
print(" ################################### ");


packageRepos = [["json-c" ,"git://github.com/json-c/json-c.git", "json-c-dir" , "", ""],
                ["libubox","git://nbd.name/luci2/libubox.git"  , "libubox-dir", "0608d1299546d4af1facc271a090cb2abb8c6105","lib-ubox-blobmsg_json.patch"],
                ["uci"    ,"git://nbd.name/uci.git"            , "uci-dir"    , "b42ee8f21842fab41a4cdf27960000bb1b3f42a7",""],
                ["ubus"   ,"git://nbd.name/luci2/ubus.git"     , "ubus-dir"   , "4e82a1fabb87b5e3c948a792e16b0fac3702721b",""],
               ];

packageConf =  [["json-c"   , "autoreconf -i && ./configure --prefix=/usr", "make" , "sudo make install", "", "sudo ln -sf /usr/include/json-c /usr/include/json"],
                ["libubox"  , "cmake CMakeLists.txt -DBUILD_LUA=OFF"    , "make" , "sudo make install", "", "sudo cp /usr/local/lib/libubox.so /usr/lib/libubox.so && sudo mkdir -p /usr/share/libubox && sudo ln -sf /usr/local/share/libubox/jshn.sh /usr/share/libubox/jshn.sh"],
                ["uci"      , "cmake CMakeLists.txt -DBUILD_LUA=OFF"    , "make" , "class=\"western\" && sudo make install", "","sudo ln -sf /usr/local/lib/libuci.so /usr/lib/libuci.so"],
                ["ubus"     , "cmake CMakeLists.txt -DBUILD_LUA=OFF"    , "make" , "sudo make install", "", "sudo ln -sf /usr/local/sbin/ubusd /usr/sbin/ubusd && sudo ln -sf /usr/local/lib/libubus.so /usr/lib/libubus.so"],
               ];

class reposInstall:
    packageName     = 0
    gitUrl          = 1
    gitDir          = 2
    checkoutVersion = 3
    patchDir        = 4

class packageConfig:
    packageName         = 0
    packageConfigure    = 1
    packageBuild        = 2
    packageInstall      = 3
    packageDirInstall   = 4
    packagePostInstall  = 5

def gitCheckout(__packageName__):
    print("fetching package : ", __packageName__);

    for idx in range(4):
        if (__packageName__ == packageRepos[idx][reposInstall.packageName]):
            print ("package got", __packageName__);
            break;

    Repo.clone_from(packageRepos[idx][reposInstall.gitUrl], packageRepos[idx][reposInstall.gitDir])

    if (packageRepos[idx][reposInstall.checkoutVersion] != ""):
        cmd = "cd " + str(packageRepos[idx][reposInstall.gitDir]) + " && git checkout master && git checkout " + str(packageRepos[idx][reposInstall.checkoutVersion]) + " && cd ..";
        os.system(cmd);
    #print("retrieving package name : ", repos)
    if (packageRepos[idx][reposInstall.patchDir] != ""):
        cmd = "cd " + str(packageRepos[idx][reposInstall.gitDir]) + " && cp ../patches/" + str(packageRepos[idx][reposInstall.patchDir]) +\
                      " . " + " && patch -p1 < " + str(packageRepos[idx][reposInstall.patchDir]);
        print ("command : ", cmd);
        os.system(cmd);

def configureAndCompile(__packageName__):
    print("configure and building : ", __packageName__);
    for idx in range(4):
        if (__packageName__ ==  packageRepos[idx][reposInstall.packageName]):
            print ("package got", __packageName__);
            break;

    cmd = "cd " + str(packageRepos[idx][reposInstall.gitDir]) + " && " + str(packageConf[idx][packageConfig.packageConfigure]) + " && " + str(packageConf[idx][packageConfig.packageBuild]);
    os.system(cmd);
    cmd = "cd " + str(packageRepos[idx][reposInstall.gitDir]) + " && " + str(packageConf[idx][packageConfig.packageInstall]) + " && " + str(packageConf[idx][packageConfig.packagePostInstall])
    os.system(cmd);

print("init fetching repos :");


gitCheckout("json-c");
configureAndCompile("json-c")

gitCheckout("libubox")
configureAndCompile("libubox");

gitCheckout("ubus")
configureAndCompile("ubus");
