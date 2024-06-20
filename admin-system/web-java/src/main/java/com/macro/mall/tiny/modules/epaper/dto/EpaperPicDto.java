package com.macro.mall.tiny.modules.epaper.dto;

import com.macro.mall.tiny.modules.epaper.model.EpaperOriginal;
import com.macro.mall.tiny.modules.epaper.model.EpaperPic;
import lombok.Data;

/**
 * @author Ymri
 * @version 1.0
 * @since 2024/4/6 15:22
 * EpaperPicDto
 */
@Data
public class EpaperPicDto extends EpaperPic {


    private EpaperOriginal epaperOriginal;

}
