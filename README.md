# m3u8_DL_tool
一个特定场景使用的 m3u8 下载脚本。
使用环境：[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-CLI)，[ffmgpe](https://ffmpeg.org/download.html)，[mp4decrypt](https://www.bento4.com/downloads/)，python3.11，mac m1。

实现功能：
1.你填一个 m3u8 链接然后下载它。
2.解析 m3u8 中的 key.url，然后构建 key 的下载链接并下载它。
3.构建一个命令用 N_m3u8DL-RE 下载视频，并且输出运行过程。

最后，别老是用这个脚本。
