package com.macro.mall.tiny.modules.epaper.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.macro.mall.tiny.modules.epaper.model.EpaperOriginal;
import com.baomidou.mybatisplus.extension.service.IService;
import com.macro.mall.tiny.modules.ums.model.UmsAdmin;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

/**
 * <p>
 * 服务类
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
public interface EpaperOriginalService extends IService<EpaperOriginal> {

    Page<EpaperOriginal> list(String keyword, Integer pageSize, Integer pageNum);

    boolean delete(Integer id);

    List<UmsAdmin> getPushUser();
    EpaperOriginal create(EpaperOriginal epaperOriginal);

    boolean showPic(Integer id, HttpServletResponse response);

    boolean uploadPic(Integer id, MultipartFile img) throws IOException;
}
