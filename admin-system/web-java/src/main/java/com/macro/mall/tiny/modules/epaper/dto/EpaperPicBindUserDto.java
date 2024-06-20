package com.macro.mall.tiny.modules.epaper.dto;

import jakarta.validation.constraints.NotEmpty;
import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.Date;

/**
 * @author Ymri
 * @version 1.0
 * @since 2024/4/10 22:52
 * EpaperPicBindUser
 */
@Getter
@Setter
public class EpaperPicBindUserDto implements Serializable {

    @NotEmpty
    private Long userId;
    @NotEmpty
    private Integer picId;
    // 推送的时间
    @NotEmpty
    private Date bindTime;

}
