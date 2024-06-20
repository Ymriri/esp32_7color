package com.macro.mall.tiny.security.util;


import cn.hutool.core.io.resource.ResourceUtil;
import cn.hutool.core.util.StrUtil;
import jakarta.servlet.ServletOutputStream;
import jakarta.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.InputStream;

/**
 * @author Ymri
 * @version 1.0
 * @since 2024/4/7 20:27
 * YmriUtils
 */
@Component
public class YmriUtils {

    @Value("${picfile.path}")
    public String fileHead;

    @Value("${picfile.tempOut}")
    public String tempPath;

    @Value("${picfile.pythonPath}")
    public String pythonPath;

    @Value("${picfile.calendarPath}")
    public String calendarPath;

    @Value("${picfile.coverPath}")
    public String coverPath;
    private static final Logger LOGGER = LoggerFactory.getLogger(YmriUtils.class);

    /**
     * 往response中写入图片
     *
     * @param filePath file_path
     * @param response response
     */
    public boolean showPic(String filePath, HttpServletResponse response) throws IOException {
        ServletOutputStream outputStream = null;
        InputStream inputStream = null;
        try {
            if (StrUtil.isNotEmpty(filePath)) {
                inputStream = ResourceUtil.getStream(this.fileHead + filePath);
            } else {
                return false;
            }
            response.setContentType("image/png");
            outputStream = response.getOutputStream();
            int len = 0;
            byte[] buffer = new byte[4096];
            while ((len = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, len);
            }
            outputStream.flush();
        } catch (Exception e) {
            LOGGER.error("showPic error", e);
        } finally {
            assert outputStream != null;
            outputStream.close();
            inputStream.close();
        }
        return true;
    }

    public boolean showAbsPic(String filePath, HttpServletResponse response) throws IOException {
        ServletOutputStream outputStream = null;
        InputStream inputStream = null;
        try {
            if (StrUtil.isNotEmpty(filePath)) {
                inputStream = ResourceUtil.getStream(filePath);
            } else {
                return false;
            }
            response.setContentType("image/png");
            outputStream = response.getOutputStream();
            int len = 0;
            byte[] buffer = new byte[4096];
            while ((len = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, len);
            }
            outputStream.flush();
        } catch (Exception e) {
            LOGGER.error(filePath);
            LOGGER.error("showPic error", e);
        } finally {
            assert outputStream != null;
            outputStream.close();
            inputStream.close();
        }
        return true;
    }

    /**
     * 往response 中写入bin数据
     *
     * @param filePath
     * @param response
     * @return
     * @throws Exception
     */
    public boolean showBin(String filePath, HttpServletResponse response) throws Exception {
        ServletOutputStream outputStream = null;
        InputStream inputStream = null;
        try {
            if (StrUtil.isNotEmpty(filePath)) {
                inputStream = ResourceUtil.getStream(filePath);
            } else {
                return false;
            }
            // 添加长度
            response.setContentLength(inputStream.available());
            response.setContentType("application/octet-stream");
            outputStream = response.getOutputStream();
            int len = 0;
            byte[] buffer = new byte[4096];
            while ((len = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, len);
            }
            outputStream.flush();
        } catch (Exception e) {
            LOGGER.error("showPic getBin", e);
        } finally {
            assert outputStream != null;
            outputStream.close();
            inputStream.close();
        }
        return true;
    }

}
