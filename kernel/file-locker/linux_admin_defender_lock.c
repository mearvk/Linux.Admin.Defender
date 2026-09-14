// SPDX-License-Identifier: GPL-2.0
/*
 * Linux.Admin.Defender - kernel file-lock reference driver
 *
 * This is a small administrative reference module.  It resolves one
 * administrator-selected filesystem path and sets the inode immutable flag.
 * The intent is protection of a known file, not transparent surveillance or
 * interception of arbitrary processes.
 *
 * Build against the running kernel with the supplied Makefile.
 *
 * Example:
 *   sudo insmod linux_admin_defender_lock.ko target=/etc/example.conf
 *
 * The immutable flag is a filesystem/inode feature and support varies by
 * filesystem.  On filesystems that do not persist the flag, use the
 * filesystem's documented file-attribute interface instead.
 */

#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/namei.h>
#include <linux/path.h>
#include <linux/string.h>

#define DRIVER_NAME "linux_admin_defender_lock"

static char *target;
module_param(target, charp, 0400);
MODULE_PARM_DESC(target, "Absolute path of the file or directory to protect");

static int __init defender_lock_init(void)
{
    struct path resolved;
    struct inode *inode;
    int ret;

    if (!target || target[0] != '/') {
        pr_err(DRIVER_NAME ": target must be an absolute path\n");
        return -EINVAL;
    }

    ret = kern_path(target, LOOKUP_FOLLOW, &resolved);
    if (ret) {
        pr_err(DRIVER_NAME ": cannot resolve %s: %d\n", target, ret);
        return ret;
    }

    inode = d_inode(resolved.dentry);
    if (!inode) {
        path_put(&resolved);
        return -ENOENT;
    }

    /*
     * inode_lock() is the VFS lock used while changing inode attributes.
     * S_IMMUTABLE is the in-kernel immutable state used by supported
     * filesystems.  mark_inode_dirty_sync() asks the filesystem to persist
     * the metadata change where the filesystem implements it.
     */
    inode_lock(inode);
    inode->i_flags |= S_IMMUTABLE;
    mark_inode_dirty_sync(inode);
    inode_unlock(inode);

    path_put(&resolved);

    pr_info(DRIVER_NAME ": protected %s\n", target);
    return 0;
}

static void __exit defender_lock_exit(void)
{
    /*
     * Deliberately do not clear S_IMMUTABLE on unload.  Unloading the driver
     * must not silently weaken a protection decision already made by the
     * administrator.  Remove the flag explicitly with the filesystem's
     * supported administrative interface (for example: chattr -i).
     */
    pr_info(DRIVER_NAME ": unloaded; existing inode protection was retained\n");
}

module_init(defender_lock_init);
module_exit(defender_lock_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MEARVK LLC");
MODULE_DESCRIPTION("Administrative immutable-file protection reference driver");
MODULE_VERSION("0.1");
